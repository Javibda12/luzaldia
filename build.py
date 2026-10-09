#!/usr/bin/env python3
"""Luz al Día: genera la web estática con el precio de la luz (PVPC) de hoy y mañana.

Uso:
  python3 build.py          -> descarga precios de Red Eléctrica y genera site/
  python3 build.py --demo   -> genera con precios inventados (para probar sin internet)

Se ejecuta solo cada hora con GitHub Actions (.github/workflows/actualizar.yml).
"""
import os, sys, json, math, shutil, datetime, urllib.request
from zoneinfo import ZoneInfo
from articles import ARTICLES
from legal import LEGAL_PAGES

# ---------------- CONFIGURACIÓN: cambia esto ----------------
SITE_NAME = "Luz al Día"
DOMAIN = os.environ.get("SITE_DOMAIN", "https://www.TUDOMINIO.es")
EMAIL = "contacto@TUDOMINIO.es"
AUTHOR = "Javi"
# Cuando AdSense te apruebe, pega aquí su <script> (o define la variable ADSENSE_CLIENT=ca-pub-XXXX)
ADSENSE_CLIENT = os.environ.get("ADSENSE_CLIENT", "")
# ------------------------------------------------------------

TZ = ZoneInfo("Europe/Madrid")
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "site")
DATA = os.path.join(BASE, "data")
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
REE = ("https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real"
       "?start_date={d}T00:00&end_date={d}T23:59&time_trunc=hour")


def fecha_larga(d):
    return f"{DIAS[d.weekday()]} {d.day} de {MESES[d.month - 1]} de {d.year}"


# ---------------- DATOS ----------------
def descargar(d):
    """Devuelve lista de (hora, €/kWh) del PVPC para el día d, o None si aún no está publicado."""
    url = REE.format(d=d.isoformat())
    req = urllib.request.Request(url, headers={"User-Agent": "LuzAlDia/1.0", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            js = json.load(r)
    except Exception as e:
        print(f"Aviso: no se pudieron descargar los precios de {d}: {e}")
        return None
    serie = next((i for i in js.get("included", []) if i.get("type") == "PVPC"
                  or i.get("attributes", {}).get("title") == "PVPC"), None)
    if not serie:
        return None
    por_hora = {}
    for v in serie["attributes"]["values"]:
        dt = datetime.datetime.fromisoformat(v["datetime"]).astimezone(TZ)
        if dt.date() != d:
            continue
        por_hora.setdefault(dt.hour, []).append(v["value"] / 1000)  # €/MWh -> €/kWh
    if len(por_hora) < 20:
        return None
    return [(h, sum(vals) / len(vals)) for h, vals in sorted(por_hora.items())]


def demo(d):
    rnd = (d.toordinal() % 7) * 0.004
    out = []
    for h in range(24):
        base = 0.11 + 0.06 * math.exp(-((h - 9.5) ** 2) / 4) + 0.09 * math.exp(-((h - 20.5) ** 2) / 5)
        base -= 0.05 * math.exp(-((h - 14.5) ** 2) / 6)  # bajada por la solar
        out.append((h, round(base + rnd, 5)))
    return out


def precios(d, modo_demo):
    os.makedirs(DATA, exist_ok=True)
    f = os.path.join(DATA, f"{d.isoformat()}.json")
    if os.path.exists(f) and not modo_demo:
        with open(f) as fh:
            return [tuple(x) for x in json.load(fh)]
    p = demo(d) if modo_demo else descargar(d)
    if p and not modo_demo:
        with open(f, "w") as fh:
            json.dump(p, fh)
    return p


def tramo(d, h):
    """Tramo de peajes de la tarifa 2.0TD (sin contar festivos nacionales)."""
    if d.weekday() >= 5 or h < 8:
        return "Valle"
    if 10 <= h < 14 or 18 <= h < 22:
        return "Punta"
    return "Llano"


def mejor_ventana(p, horas):
    mejor = None
    for i in range(len(p) - horas + 1):
        m = sum(x[1] for x in p[i:i + horas]) / horas
        if mejor is None or m < mejor[1]:
            mejor = (p[i][0], m)
    return mejor


# ---------------- HTML ----------------
CSS = open(os.path.join(BASE, "estilo.css"), encoding="utf-8").read()

COOKIE_JS = """<script>(function(){var K='cookie_consent';function g(){try{return localStorage.getItem(K)}catch(e){return null}}
function s(v){try{localStorage.setItem(K,v)}catch(e){}}var b=document.getElementById('cookie-banner');if(!g()&&b){b.style.display='block'}
window.cookieChoice=function(v){s(v);if(b)b.style.display='none'};})();</script>"""


def page(title, body, description, path, head_extra=""):
    root = "../" * path.count("/")
    ads = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>'
           if ADSENSE_CLIENT else "<!-- AdSense: define ADSENSE_CLIENT cuando te aprueben -->")
    nav = (f'<a href="{root}index.html">Precio hoy</a><a href="{root}precio-luz-manana.html">Mañana</a>'
           f'<a href="{root}guias.html">Guías de ahorro</a>')
    legal = "".join(f'<a href="{root}{p["slug"]}.html">{p["title"]}</a>' for p in LEGAL_PAGES)
    year = datetime.date.today().year
    return f"""<!doctype html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{description}">
<link rel="canonical" href="{DOMAIN}/{'' if path == 'index.html' else path}">
<link rel="stylesheet" href="{root}estilo.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚡</text></svg>">
{head_extra}{ads}
</head><body>
<header class="site"><div class="wrap wide"><a class="logo" href="{root}index.html">Luz <span>al Día</span></a><nav>{nav}</nav></div></header>
<main>{body}</main>
<footer class="site"><div class="wrap wide">
<p>© {year} {SITE_NAME}. Precios del PVPC (tarifa 2.0TD) con datos públicos de Red Eléctrica de España. Impuestos no incluidos.</p>
<p><a href="{root}sobre-nosotros.html">Sobre nosotros</a><a href="{root}contacto.html">Contacto</a>{legal}</p>
</div></footer>
<div id="cookie-banner"><div class="wrap wide"><span>Usamos cookies propias y de Google para mostrar anuncios y medir el tráfico. <a href="{root}politica-de-cookies.html">Más información</a>.</span>
<span><button class="btn-no" onclick="cookieChoice('rechazadas')">Rechazar</button> <button class="btn-ok" onclick="cookieChoice('aceptadas')">Aceptar</button></span></div></div>
{COOKIE_JS}</body></html>"""


def fill(t):
    return (t.replace("{SITE}", SITE_NAME).replace("{EMAIL}", EMAIL).replace("{DOMAIN}", DOMAIN)
            .replace("{AUTHOR}", AUTHOR).replace("{TODAY}", datetime.date.today().isoformat()))


def eur(x):
    return f"{x:.4f}".replace(".", ",")


def bloque_precios(d, p, es_hoy):
    vals = [v for _, v in p]
    media = sum(vals) / len(vals)
    lo, hi = min(p, key=lambda x: x[1]), max(p, key=lambda x: x[1])
    ordenadas = sorted(vals)
    t1, t2 = ordenadas[len(vals) // 3], ordenadas[2 * len(vals) // 3]
    nivel = lambda v: "barata" if v < t1 else ("cara" if v >= t2 else "media")
    ahora = datetime.datetime.now(TZ).hour if es_hoy else None
    v2, v3 = mejor_ventana(p, 2), mejor_ventana(p, 3)

    barras = "".join(
        f'<div class="bar {nivel(v)}{" now" if h == ahora else ""}" style="height:{max(6, 100 * v / hi[1]):.0f}%" '
        f'title="{h:02d}:00 · {eur(v)} €/kWh"><span>{h}</span></div>' for h, v in p)
    filas = "".join(
        f'<tr class="{nivel(v)}{" now" if h == ahora else ""}"><td>{h:02d}:00 – {(h + 1) % 24:02d}:00</td>'
        f'<td><strong>{eur(v)}</strong> €/kWh</td><td>{tramo(d, h)}</td><td><span class="tag {nivel(v)}">{nivel(v).capitalize()}</span></td></tr>'
        for h, v in p)
    ahora_txt = ""
    if es_hoy and ahora is not None:
        va = dict(p).get(ahora)
        if va is not None:
            ahora_txt = (f'<div class="stat big"><span>Ahora ({ahora:02d}:00 – {(ahora + 1) % 24:02d}:00)</span>'
                         f'<strong>{eur(va)} €/kWh</strong><em class="tag {nivel(va)}">{nivel(va)}</em></div>')
    return f"""
<div class="stats">{ahora_txt}
<div class="stat"><span>Precio medio</span><strong>{eur(media)} €/kWh</strong></div>
<div class="stat"><span>Hora más barata</span><strong>{lo[0]:02d}:00 · {eur(lo[1])}</strong></div>
<div class="stat"><span>Hora más cara</span><strong>{hi[0]:02d}:00 · {eur(hi[1])}</strong></div>
</div>
<div class="chart" aria-label="Precio por horas">{barras}</div>
<p class="legend"><span class="tag barata">Barata</span> <span class="tag media">Media</span> <span class="tag cara">Cara</span> · Precio del término de energía del PVPC, sin impuestos.</p>
<div class="tip box"><strong>Mejores horas para tus electrodomésticos</strong>
Lavadora o lavavajillas (2 h): de <b>{v2[0]:02d}:00 a {(v2[0] + 2) % 24:02d}:00</b> (media {eur(v2[1])} €/kWh).<br>
Secadora, horno o carga del coche (3 h): de <b>{v3[0]:02d}:00 a {(v3[0] + 3) % 24:02d}:00</b> (media {eur(v3[1])} €/kWh).<br>
Evita, si puedes, las <b>{hi[0]:02d}:00</b>: es la hora más cara del día.</div>
<div class="ad-slot"></div>
<h2>Precio de la luz por horas · {fecha_larga(d)}</h2>
<table class="prices"><thead><tr><th>Hora</th><th>Precio</th><th>Tramo 2.0TD</th><th>Nivel</th></tr></thead><tbody>{filas}</tbody></table>
"""


def pagina_hoy(d, p, pm):
    if p:
        datos = bloque_precios(d, p, True)
    else:
        datos = '<div class="warn box"><strong>Actualizando precios</strong>Los precios de hoy se están descargando. Vuelve a cargar la página en unos minutos.</div>'
    manana_link = ('<p><a class="btn" href="precio-luz-manana.html">Ver el precio de la luz de mañana →</a></p>' if pm else
                   '<p class="muted">El precio de mañana lo publica Red Eléctrica cada tarde, normalmente a partir de las 20:15. Esta página se actualiza sola.</p>')
    body = f"""<section class="hero"><div class="wrap">
<h1>Precio de la luz hoy, {fecha_larga(d)}</h1>
<p>Precio por horas del PVPC (tarifa regulada 2.0TD) en la península, actualizado automáticamente con los datos oficiales de Red Eléctrica.</p>
</div></section>
<div class="wrap">{datos}{manana_link}
<h2>Cómo leer esta tabla</h2>
<p>Si tienes contratada la <strong>tarifa regulada PVPC</strong>, pagas la energía a un precio distinto cada hora. Los precios de esta página son el término de energía (incluye peajes y cargos), sin el impuesto eléctrico ni el IVA. Si tienes una tarifa de <strong>mercado libre</strong> con precio fijo, el precio horario no te afecta, pero puedes usarlo para saber si tu tarifa te compensa: lo explicamos en <a href="pvpc-o-mercado-libre.html">PVPC o mercado libre: cuál conviene</a>.</p>
<h2>Guías para pagar menos</h2><div class="grid">{''.join(card(a) for a in ARTICLES[:4])}</div>
</div>"""
    faq = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
           '{"@type":"Question","name":"¿A qué hora es más barata la luz hoy?","acceptedAnswer":{"@type":"Answer","text":"'
           + (f'Hoy la hora más barata es a las {min(p, key=lambda x: x[1])[0]:02d}:00.' if p else 'Consulta la tabla de precios por horas.')
           + '"}},{"@type":"Question","name":"¿Cuándo se publica el precio de la luz de mañana?","acceptedAnswer":{"@type":"Answer","text":"Red Eléctrica publica los precios del día siguiente cada tarde, normalmente a partir de las 20:15."}}]}</script>')
    return page(f"Precio de la luz hoy {d.day} de {MESES[d.month - 1]} por horas | {SITE_NAME}", body,
                f"Precio de la luz hoy {fecha_larga(d)} por horas: hora más barata, más cara y mejores horas para poner la lavadora. PVPC actualizado.",
                "index.html", faq)


def pagina_manana(d, p):
    if p:
        datos = bloque_precios(d, p, False)
    else:
        datos = ('<div class="warn box"><strong>Todavía no se ha publicado</strong>Red Eléctrica publica el precio de la luz de mañana '
                 'cada tarde, normalmente a partir de las 20:15. Esta página se actualiza sola: vuelve más tarde.</div>')
    body = f"""<section class="hero"><div class="wrap"><h1>Precio de la luz mañana, {fecha_larga(d)}</h1>
<p>Planifica la lavadora, el lavavajillas o la carga del coche con el precio por horas del PVPC de mañana.</p></div></section>
<div class="wrap">{datos}<p><a class="btn" href="index.html">← Volver al precio de hoy</a></p></div>"""
    return page(f"Precio de la luz mañana {d.day} de {MESES[d.month - 1]} por horas | {SITE_NAME}", body,
                f"Precio de la luz mañana {fecha_larga(d)}: horas más baratas y más caras del PVPC para organizar tu consumo.",
                "precio-luz-manana.html")


def card(a):
    return f'<a class="card" href="{a["slug"]}.html"><h3>{a["title"]}</h3><p>{a["description"]}</p></a>'


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


SOBRE = """<p>{SITE} nace para que cualquiera pueda saber, de un vistazo, cuándo le sale más barato encender la lavadora, el horno o la calefacción.</p>
<p>La web la lleva {AUTHOR}, técnico de mantenimiento. En el día a día veo cómo pequeños cambios de horario y un buen mantenimiento de los aparatos se notan mucho en la factura, y aquí lo cuento de forma sencilla.</p>
<p>Los precios se obtienen automáticamente de los datos públicos de Red Eléctrica de España. Las guías las escribo y reviso yo. Si ves un error, escríbeme a <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>"""
CONTACTO = """<p>Para dudas, errores o colaboraciones escribe a <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p>No gestionamos contratos ni podemos cambiarte de compañía: para eso contacta con tu comercializadora.</p>"""


def main():
    modo_demo = "--demo" in sys.argv
    hoy = datetime.datetime.now(TZ).date()
    manana = hoy + datetime.timedelta(days=1)
    p_hoy, p_man = precios(hoy, modo_demo), precios(manana, modo_demo)

    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    write("estilo.css", CSS)
    write("index.html", pagina_hoy(hoy, p_hoy, p_man))
    write("precio-luz-manana.html", pagina_manana(manana, p_man))
    urls = ["", "precio-luz-manana.html", "guias.html"]

    write("guias.html", page(f"Guías para ahorrar en la factura de la luz | {SITE_NAME}",
          f'<section class="hero"><div class="wrap"><h1>Guías para ahorrar en la luz</h1><p>Trucos prácticos para pagar menos sin pasar frío ni dejar de usar tus electrodomésticos.</p></div></section><div class="wrap"><div class="grid">{"".join(card(a) for a in ARTICLES)}</div></div>',
          "Guías prácticas para ahorrar en la factura de la luz: horarios, tarifas, consumo de electrodomésticos y calefacción.", "guias.html"))

    for a in ARTICLES:
        rel = [r for r in ARTICLES if r["slug"] != a["slug"]][:3]
        schema = (f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{a["title"]}",'
                  f'"inLanguage":"es","author":{{"@type":"Person","name":"{AUTHOR}"}},"publisher":{{"@type":"Organization","name":"{SITE_NAME}"}}}}</script>')
        body = (f'<article><div class="wrap"><h1>{a["title"]}</h1><p class="meta">Por {AUTHOR} · Lectura de {a["minutes"]} min</p>'
                f'<div class="cta box">⚡ <a href="index.html">Consulta aquí el precio de la luz de hoy por horas</a></div>'
                f'{fill(a["html"])}<div class="related"><h2>Sigue leyendo</h2><div class="grid">{"".join(card(r) for r in rel)}</div></div></div></article>')
        write(f'{a["slug"]}.html', page(f'{a["title"]} | {SITE_NAME}', body, a["description"], f'{a["slug"]}.html', schema))
        urls.append(f'{a["slug"]}.html')

    for lp in LEGAL_PAGES + [{"slug": "sobre-nosotros", "title": "Sobre nosotros", "html": SOBRE},
                             {"slug": "contacto", "title": "Contacto", "html": CONTACTO}]:
        write(f'{lp["slug"]}.html', page(f'{lp["title"]} | {SITE_NAME}',
              f'<article><div class="wrap"><h1>{lp["title"]}</h1>{fill(lp["html"])}</div></article>',
              f'{lp["title"]} de {SITE_NAME}.', f'{lp["slug"]}.html'))
        urls.append(f'{lp["slug"]}.html')

    today = hoy.isoformat()
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          + "".join(f"<url><loc>{DOMAIN}/{u}</loc><lastmod>{today}</lastmod></url>" for u in urls) + "</urlset>\n")
    pub = ADSENSE_CLIENT.replace("ca-", "") if ADSENSE_CLIENT else "pub-XXXXXXXXXXXXXXXX"
    write("ads.txt", f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")
    if DOMAIN.startswith("https://") and "TUDOMINIO" not in DOMAIN:
        write("CNAME", DOMAIN.replace("https://", "").rstrip("/") + "\n")
    print(f"OK: {len(urls)} páginas · hoy={'sí' if p_hoy else 'no'} · mañana={'sí' if p_man else 'no'}")


if __name__ == "__main__":
    main()

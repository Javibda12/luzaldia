# Luz al Día: cómo ponerla en marcha

La web muestra cada día el **precio de la luz de hoy y de mañana por horas** (PVPC) con datos de Red Eléctrica, y se actualiza sola cada hora. Alojarla es gratis con GitHub Pages; solo pagas el dominio.

## 1. Compra el dominio (unos 10 € al año)
Busca uno corto en DonDominio, Namecheap o Cloudflare. Ideas: `luzaldia.es`, `preciodelaluzhoyya.es`, `laluzhoy.es` (comprueba que estén libres).

## 2. Sube la web a GitHub (gratis)
1. Crea una cuenta en github.com.
2. Crea un repositorio **público** llamado, por ejemplo, `luzaldia`.
3. Pulsa «uploading an existing file» y arrastra **todo el contenido** de esta carpeta (incluida la carpeta `.github`; si tu ordenador la oculta, actívalo para ver archivos ocultos).
4. En el repositorio: **Settings → Pages → Source: GitHub Actions**.
5. En **Settings → Secrets and variables → Actions → Variables**, crea la variable `SITE_DOMAIN` con tu dominio, por ejemplo `https://www.luzaldia.es`.
6. Ve a **Actions → Actualizar precios y publicar → Run workflow**. En un par de minutos la web estará publicada y desde entonces se actualiza cada hora.

## 3. Conecta el dominio
En **Settings → Pages → Custom domain** escribe tu dominio. GitHub te dice qué registros DNS poner en tu proveedor de dominio (un CNAME para `www` y cuatro registros A para el dominio raíz). Activa «Enforce HTTPS».

## 4. Rellena tus datos
Antes de pedir AdSense, edita `legal.py` y cambia `[TU NOMBRE Y APELLIDOS]`, `[TU NIF]` y `[TU DIRECCIÓN O LOCALIDAD]`. En `build.py` cambia `EMAIL`.

## 5. Google Search Console
Date de alta en search.google.com/search-console, verifica el dominio y envía `sitemap.xml`. Es lo que hace que Google te encuentre antes.

## 6. AdSense
Cuando la web lleve unas semanas publicada y con visitas, solicita AdSense en adsense.google.com. Al aprobarte:
- Crea la variable `ADSENSE_CLIENT` con tu código (`ca-pub-XXXXXXXXXXXXXXXX`). El `ads.txt` y el script se generan solos.
- En AdSense, activa los **anuncios automáticos** y, en «Privacidad y mensajes», el mensaje de consentimiento para Europa.

## Probar en tu ordenador
```
python3 build.py --demo
```
Genera la web con precios inventados en la carpeta `site/`. Abre `site/index.html` en el navegador.

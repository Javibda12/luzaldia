"""Páginas legales (RGPD, LSSI-CE y requisitos de Google AdSense).

IMPORTANTE: rellena los datos entre [CORCHETES] antes de publicar. Son plantillas
orientativas, no asesoramiento legal.
"""

AVISO_LEGAL = """
<p>En cumplimiento de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de este sitio web:</p>
<ul>
<li><strong>Titular:</strong> [TU NOMBRE Y APELLIDOS]</li>
<li><strong>NIF:</strong> [TU NIF]</li>
<li><strong>Domicilio:</strong> [TU DIRECCIÓN O LOCALIDAD]</li>
<li><strong>Email:</strong> {EMAIL}</li>
<li><strong>Sitio web:</strong> {DOMAIN}</li>
</ul>
<h2>Objeto</h2>
<p>{SITE} es un sitio divulgativo que muestra el precio horario de la electricidad a partir de datos públicos de Red Eléctrica de España y publica guías de ahorro. La información se ofrece con fines orientativos: el precio final de tu factura depende de tu contrato.</p>
<h2>Responsabilidad</h2>
<p>Los precios se obtienen de forma automática de fuentes públicas y pueden contener retrasos o errores puntuales. Consulta siempre los datos oficiales y tu contrato antes de tomar decisiones. Los trabajos con gas o en la instalación eléctrica deben realizarlos profesionales autorizados.</p>
<h2>Propiedad intelectual</h2>
<p>Los textos e imágenes propios de este sitio pertenecen a su titular. No se permite su reproducción total o parcial sin autorización, salvo citas breves con enlace a la fuente.</p>
<h2>Enlaces y publicidad</h2>
<p>Este sitio muestra publicidad de Google AdSense y puede incluir enlaces de afiliado, por los que el titular puede recibir una comisión sin coste adicional para el usuario.</p>
"""

PRIVACIDAD = """
<p>Última actualización: {TODAY}</p>
<h2>Responsable del tratamiento</h2>
<p>[TU NOMBRE Y APELLIDOS], con email {EMAIL}.</p>
<h2>Qué datos recogemos</h2>
<ul>
<li><strong>Datos que nos envías:</strong> si nos escribes por email, tu dirección y el contenido del mensaje, solo para responderte.</li>
<li><strong>Datos de navegación:</strong> mediante cookies, según se explica en la <a href="politica-de-cookies.html">política de cookies</a>.</li>
</ul>
<h2>Base legal</h2>
<p>Tu consentimiento (al escribirnos o aceptar cookies) y el interés legítimo en mantener el sitio seguro y funcionando.</p>
<h2>Publicidad de Google</h2>
<p>Este sitio usa Google AdSense. Google y sus socios utilizan cookies para mostrar anuncios basados en tus visitas anteriores a este y otros sitios web. Puedes desactivar la publicidad personalizada en <a href="https://adssettings.google.com" rel="nofollow">la configuración de anuncios de Google</a>. Más información sobre cómo usa Google los datos en <a href="https://policies.google.com/technologies/partner-sites" rel="nofollow">policies.google.com/technologies/partner-sites</a>.</p>
<h2>Conservación y cesión</h2>
<p>Los emails se conservan el tiempo necesario para atender tu consulta. No cedemos datos a terceros salvo obligación legal o los proveedores técnicos indicados (alojamiento web y Google).</p>
<h2>Tus derechos</h2>
<p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a {EMAIL}. También puedes reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>
"""

COOKIES = """
<p>Una cookie es un pequeño archivo que el navegador guarda al visitar una web. Este sitio utiliza:</p>
<table>
<tr><th>Cookie</th><th>Tipo</th><th>Finalidad</th><th>Titular</th></tr>
<tr><td>cookie_consent</td><td>Técnica (almacenamiento local)</td><td>Recordar si aceptaste o rechazaste las cookies</td><td>{SITE}</td></tr>
<tr><td>Cookies de Google AdSense (por ejemplo __gads, IDE)</td><td>Publicidad</td><td>Mostrar anuncios y medir su rendimiento</td><td>Google</td></tr>
</table>
<h2>Cómo gestionarlas</h2>
<p>Al entrar puedes aceptar o rechazar las cookies no técnicas en el aviso inferior. También puedes borrarlas o bloquearlas desde la configuración de tu navegador (Chrome, Firefox, Safari, Edge).</p>
<p>Al activar AdSense, Google ofrece un mensaje de consentimiento certificado (CMP) desde el panel «Privacidad y mensajes»; se recomienda activarlo para el tráfico europeo, ya que Google lo exige para mostrar anuncios en el Espacio Económico Europeo.</p>
"""

LEGAL_PAGES = [
    {"slug": "aviso-legal", "title": "Aviso legal", "html": AVISO_LEGAL},
    {"slug": "politica-de-privacidad", "title": "Política de privacidad", "html": PRIVACIDAD},
    {"slug": "politica-de-cookies", "title": "Política de cookies", "html": COOKIES},
]

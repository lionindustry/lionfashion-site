#!/usr/bin/env python3
"""Builds the Lion Fashion website into public/ (English pages + Spanish pages under /es/).

Edit the English text here or in source/sections.html, add the Spanish for any new text to
ES_NEW below (or source/es_base.json), then run:   python3 tools/build.py
The build stops and lists any English text that has no Spanish translation.
"""
import json, os, re, shutil, sys, html
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'source')
OUT = os.path.join(ROOT, 'public')

DOMAIN = os.environ.get('LF_DOMAIN') or open(os.path.join(SRC, 'DOMAIN')).read().strip()   # e.g. lionfashion.com
SITE = f'https://{DOMAIN}'
TODAY = date.today().isoformat()
EMAIL = 'sales@lionfashionglobal.com'
WA = '+1 314 250 8276'
WA_NUM = '13142508276'
IMGV = '2'   # raise when a product photo is replaced under the same name, so browsers load the new one

# ---------------------------------------------------------------- pages
# slug '' = home. Each page: titles, descriptions, nav label (EN/ES).
PAGES = [
  dict(slug='', nav=None,
       title=('Underwear OEM & ODM Manufacturer in China | Lion Fashion', 'Fabricante de ropa interior OEM y ODM en China | Lion Fashion'),
       desc=("Private-label men's, women's and thermal underwear made to your spec in Zhongshan, China. OEM, ODM and in-stock programs, OEKO-TEX certified fabrics, 35-day bulk lead time.",
             'Ropa interior de marca privada para hombre, mujer y térmica, fabricada a su medida en Zhongshan, China. Programas OEM, ODM y en stock, telas con certificación OEKO-TEX y producción en 35 días.')),
  dict(slug='mens-underwear-manufacturer', cat='men', nav=("Men's", 'Hombre'),
       title=("Men's Underwear Manufacturer: Boxers & Trunks OEM | Lion Fashion", 'Fabricante de ropa interior de hombre: bóxers OEM | Lion Fashion'),
       desc=("Private-label men's boxer briefs and trunks: seamless bonded, nylon ice silk, modal and sport styles. Your label, your packaging, 35-day bulk production in China.",
             'Bóxers de hombre con su marca: sin costuras termosellados, nailon ice silk, modal y deportivos. Su etiqueta y su empaque, producción en 35 días en China.'),
       h1=("Men's underwear manufacturer for your brand", 'Fabricante de ropa interior de hombre para su marca'),
       intro=("Boxer briefs and trunks developed for brands and retailers: seamless bonded styles, cool-touch nylon ice silk, modal and long-leg sport boxers. Pick a base style below and change the fabric, color, waistband and packaging, or send us your own tech pack.",
              'Bóxers desarrollados para marcas y cadenas minoristas: modelos sin costuras termosellados, nailon ice silk de tacto frío, modal y bóxers deportivos de pierna larga. Elija un modelo base y cambie la tela, el color, el elástico y el empaque, o envíenos su propia ficha técnica.'),
       img='f-laser.jpg'),
  dict(slug='womens-underwear-manufacturer', cat='women', nav=("Women's", 'Mujer'),
       title=("Women's Underwear Manufacturer: Briefs OEM & ODM | Lion Fashion", 'Fabricante de ropa interior de mujer: calzones OEM y ODM | Lion Fashion'),
       desc=("Private-label women's briefs in mulberry silk, Lenzing modal, Supima cotton and PLA fiber. Seamless and high-rise styles, custom waistbands and labels, made in China.",
             'Calzones de mujer con su marca en seda de morera, modal Lenzing, algodón Supima y fibra PLA. Modelos sin costura y de tiro alto, elásticos y etiquetas a medida, fabricados en China.'),
       h1=("Women's underwear manufacturer for your brand", 'Fabricante de ropa interior de mujer para su marca'),
       intro=("Briefs in mulberry silk, Lenzing modal, lyocell-modal rib, Supima cotton and plant-based PLA fiber. Every base style can change fabric, color, gusset, waistband and packaging, and our pattern team adapts sizing to your market.",
              'Calzones en seda de morera, modal Lenzing, rib de lyocell-modal, algodón Supima y fibra PLA de origen vegetal. En cada modelo base se puede cambiar la tela, el color, la entrepierna, el elástico y el empaque, y nuestro equipo de patronaje adapta las tallas a su mercado.'),
       img='f-cutting.jpg'),
  dict(slug='thermal-underwear-manufacturer', cat='thermal', nav=('Thermal', 'Térmica'),
       title=('Thermal Underwear Manufacturer: Base Layer Sets OEM | Lion Fashion', 'Fabricante de ropa interior térmica: conjuntos OEM | Lion Fashion'),
       desc=('Private-label thermal underwear: brushed cashmere-blend and combed cotton base layer sets for men and women. Your brand, your packaging, made in China.',
             'Ropa interior térmica con su marca: conjuntos de primera capa perchados con cachemira y de algodón peinado para hombre y mujer. Su marca, su empaque, fabricados en China.'),
       h1=('Thermal underwear manufacturer for your brand', 'Fabricante de ropa interior térmica para su marca'),
       intro=('Base layer tops and long johns for cold-weather ranges: brushed cashmere-blend sets at 280 g/m² and breathable combed cotton sets. Order ahead of the season; colors, weights and packaging are made to your program.',
              'Camisetas y pantalones de primera capa para colecciones de invierno: conjuntos perchados con cachemira de 280 g/m² y conjuntos transpirables de algodón peinado. Haga su pedido antes de la temporada; colores, gramajes y empaque según su programa.'),
       img='f-compactor.jpg'),
  dict(slug='factory', nav=('Factory', 'Fábrica'),
       title=('Underwear Factory in Zhongshan: Knitting to Packing | Lion Fashion', 'Fábrica de ropa interior en Zhongshan: del tejido al empaque | Lion Fashion'),
       desc=('Inside our underwear supply chain in Zhongshan, Guangdong: circular knitting, dyeing, automatic cutting, laser bonding, sewing and packing. OEKO-TEX fabrics, amfori BSCI audited, AQL 2.5.',
             'Nuestra cadena de suministro de ropa interior en Zhongshan, Guangdong: tejido circular, teñido, corte automático, termosellado láser, confección y empaque. Telas OEKO-TEX, auditoría amfori BSCI, AQL 2.5.'),
       h1=('From yarn to carton in one supply chain', 'Del hilo a la caja en una sola cadena de suministro'),
       intro=('Fabric, trims and garments are made inside the same group in Zhongshan, Guangdong. Here is what happens at each stage, the fibers we run, and how quality and compliance are checked.',
              'Telas, avíos y prendas se fabrican dentro del mismo grupo en Zhongshan, Guangdong. Esto es lo que ocurre en cada etapa, las fibras que trabajamos y cómo se controlan la calidad y el cumplimiento.')),
  dict(slug='faq', nav=('FAQ', 'Preguntas'),
       title=('Underwear OEM & ODM FAQ: MOQ, Lead Time, Samples | Lion Fashion', 'Preguntas frecuentes OEM y ODM de ropa interior: pedido mínimo, plazos, muestras | Lion Fashion'),
       desc=('Answers for brands planning a private-label underwear order: minimum order, OEM vs ODM, samples, lead time, labels and packaging, fabrics, certification, quality control and shipping.',
             'Respuestas para marcas que planean un pedido de ropa interior de marca privada: pedido mínimo, OEM vs ODM, muestras, plazos, etiquetas y empaque, telas, certificación, control de calidad y embarque.'),
       h1=('Questions buyers ask before ordering', 'Preguntas que hacen los compradores antes de pedir'),
       intro=('Short answers to what brands usually ask in the first emails. If yours is not here, send it with the quote form at the bottom of the page.',
              'Respuestas breves a lo que las marcas suelen preguntar en los primeros correos. Si su pregunta no está aquí, envíela con el formulario de cotización al final de la página.')),
]

# ---------------------------------------------------------------- products (EN, ES)
P = [
 ('men','M-SB01',['m-seamless-grey','m-seamless-black','m-seamless-navy'],("All seamless bonded boxer brief","Bóxer totalmente sin costuras termosellado"),("Nylon / spandex · bonded","Nailon / elastano · termosellado"),("Our lead men's style. Laser-cut, bonded edges with no side seams and a 3D-shaped pouch.","Nuestro modelo principal para hombre. Bordes cortados con láser y termosellados, sin costuras laterales y con bolsa frontal 3D.")),
 ('men','M-IS02',['m-icesilk-grey','m-icesilk-blue'],("Ice-silk double-layer trunk","Bóxer ice silk de doble capa"),("Nylon ice silk · double pouch","Nailon ice silk · bolsa doble"),("Cool-touch nylon with a two-layer front for support and opacity in light colors.","Nailon de tacto frío con frente de dos capas para soporte y opacidad en colores claros.")),
 ('men','M-PR03',['m-printed'],("Printed ice-silk trunk","Bóxer ice silk estampado"),("Nylon ice silk · all-over print","Nailon ice silk · estampado total"),("Your artwork printed all-over; antibacterial-finish gusset.","Su diseño estampado en toda la prenda; entrepierna con acabado antibacteriano.")),
 ('men','M-GL04',['m-glossy'],("Satin-finish trunk","Bóxer de acabado satinado"),("73% nylon · 27% spandex","73% nailon · 27% elastano"),("High-luster fabric with a soft brushed waistband.","Tela de alto brillo con elástico de cintura suave y perchado.")),
 ('men','M-UT05',['m-thin-blue','m-thin-navy'],("Ultra-thin trunk","Bóxer ultradelgado"),("120-count nylon ice silk","Nailon ice silk de 120 hilos"),("Very light summer weight that dries fast.","Peso muy ligero para verano, de secado rápido.")),
 ('men','M-SP06',['m-sport-black','m-sport-camo'],("Long-leg sport boxer","Bóxer deportivo de pierna larga"),("Micro-mesh · anti-chafe leg","Micromalla · pierna antirozaduras"),("Longer leg to stop chafing, mesh pouch and vented panels for training.","Pierna más larga para evitar rozaduras, bolsa de malla y paneles ventilados para entrenar.")),
 ('women','ZY01',['w-silk-taupe','w-silk-green'],("Mulberry silk brief","Calzón de seda de morera"),("86% mulberry silk · 14% spandex","86% seda de morera · 14% elastano"),("Seamless premium brief with an extended antibacterial-finish gusset.","Calzón premium sin costuras con entrepierna extendida de acabado antibacteriano.")),
 ('women','ZY02',['w-silkcrotch-lilac'],("Modal brief, silk gusset","Calzón de modal, entrepierna de seda"),("88% modal · 12% spandex","88% modal · 12% elastano"),("Modal body with a mulberry silk gusset lining.","Cuerpo de modal con forro de entrepierna de seda de morera.")),
 ('women','ZY03',['w-pla-lilac','w-pla-red'],("Modal brief, PLA gusset","Calzón de modal, entrepierna PLA"),("Modal · polylactic-acid gusset","Modal · entrepierna de ácido poliláctico"),("Plant-based PLA fiber gusset that wicks moisture.","Entrepierna de fibra PLA de origen vegetal que absorbe la humedad.")),
 ('women','ZY04',['w-tencel-pink'],("80S rib brief","Calzón de rib 80S"),("80S lyocell-modal rib","Rib de lyocell-modal 80S"),("Fine rib knit with contrast binding.","Tejido rib fino con ribete en contraste.")),
 ('women','ZY05',['w-lenzing-cream'],("60S Lenzing modal brief","Calzón de modal Lenzing 60S"),("60S Lenzing modal","Modal Lenzing 60S"),("Fine-gauge modal with a soft, matte surface.","Modal de galga fina con superficie suave y mate.")),
 ('women','ZY06',['w-modal-lilac'],("Seamless modal brief","Calzón de modal sin costuras"),("89% modal · 11% spandex","89% modal · 11% elastano"),("One-piece cut that stays invisible under fitted clothing.","Corte de una sola pieza que no se marca bajo ropa ajustada.")),
 ('women','ZY07',['w-pima-lilac','w-pima-black'],("Supima cotton brief","Calzón de algodón Supima"),("60S Supima cotton","Algodón Supima 60S"),("Long-staple cotton everyday brief with a cotton gusset.","Calzón de uso diario en algodón de fibra larga, con entrepierna de algodón.")),
 ('women','ZY08',['w-pima-teal','w-pima-grey'],("Supima cotton high-rise brief","Calzón tiro alto de algodón Supima"),("60S Supima cotton","Algodón Supima 60S"),("Higher rise with a wide, flat waistband.","Tiro más alto con elástico de cintura ancho y plano.")),
 ('thermal','BN01',['t-men-cashmere'],("Men's cashmere-blend thermal set","Conjunto térmico de hombre con cachemira"),("Brushed · 280 g/m²","Perchado · 280 g/m²"),("Top and long johns with a brushed interior for cold climates.","Camiseta y pantalón largo con interior perchado para climas fríos.")),
 ('thermal','BN02',['t-men-cotton'],("Men's cotton thermal set","Conjunto térmico de hombre de algodón"),("95% combed cotton","95% algodón peinado"),("Breathable crew-neck top and pants for everyday warmth.","Camiseta de cuello redondo y pantalón transpirables para el día a día.")),
 ('thermal','BN03',['t-women-cotton'],("Women's cotton thermal top","Camiseta térmica de mujer de algodón"),("Combed cotton","Algodón peinado"),("Slim long-sleeve base layer in seasonal colors.","Primera capa entallada de manga larga en colores de temporada.")),
]

# ---------------------------------------------------------------- FAQ (EN, ES)
FAQ = [
 (("What is your minimum order quantity?", "¿Cuál es su pedido mínimo?"),
  ("It depends on the style and the fabric. Styles from our library in stock fabrics can start smaller than a fully new OEM style with custom-dyed fabric. Tell us the quantity you plan per style and per color and we quote against it. For a first test order, our in-stock program with your label is usually the easiest start.",
   "Depende del modelo y de la tela. Los modelos de nuestro catálogo en telas de stock pueden empezar con cantidades menores que un modelo OEM nuevo con tela teñida a medida. Indíquenos la cantidad prevista por modelo y por color y cotizamos en base a ella. Para un primer pedido de prueba, el programa en stock con su etiqueta suele ser el inicio más sencillo.")),
 (("What is the difference between OEM and ODM?", "¿Cuál es la diferencia entre OEM y ODM?"),
  ("OEM means we produce your own design from your tech pack, size chart and reference samples. ODM means you start from one of our developed base styles and we adapt the fabric, color, waistband, gusset, labels and packaging to your brand. ODM is faster to launch because the patterns and fabrics are already proven.",
   "OEM significa que fabricamos su propio diseño a partir de su ficha técnica, tabla de medidas y muestras de referencia. ODM significa que usted parte de uno de nuestros modelos base y adaptamos la tela, el color, el elástico, la entrepierna, las etiquetas y el empaque a su marca. ODM permite lanzar más rápido porque los patrones y las telas ya están probados.")),
 (("How long does production take?", "¿Cuánto tarda la producción?"),
  ("Bulk production typically takes 35 days after you approve the pre-production sample and pay the deposit. Urgent orders from in-stock styles can ship in as little as 48 hours. Sampling time depends on whether the style is new or adapted from our library; we confirm it with the quote.",
   "La producción suele tardar 35 días después de aprobar la muestra de preproducción y pagar el anticipo. Los pedidos urgentes de modelos en stock pueden despacharse en apenas 48 horas. El tiempo de muestras depende de si el modelo es nuevo o adaptado de nuestro catálogo; lo confirmamos con la cotización.")),
 (("Can I get samples before ordering?", "¿Puedo recibir muestras antes de pedir?"),
  ("Yes. We send fabric swatches and lab dips first, then fit samples, then a pre-production sample in the final fabric with your labels. Bulk production starts only after you sign off the pre-production sample.",
   "Sí. Primero enviamos muestras de tela y lab dips, luego muestras de ajuste y después una muestra de preproducción en la tela final con sus etiquetas. La producción comienza solo después de que usted apruebe la muestra de preproducción.")),
 (("Can you add my brand labels and packaging?", "¿Pueden poner mis etiquetas y mi empaque?"),
  ("Yes, every program includes your branding: jacquard or printed waistbands with your logo, woven or heat-transfer labels, hang tags, bags and boxes. Packing follows your packing list and carton marks.",
   "Sí, todos los programas incluyen su marca: elásticos jacquard o estampados con su logo, etiquetas tejidas o transfer, etiquetas colgantes, bolsas y cajas. El empaque sigue su packing list y las marcas de sus cajas.")),
 (("Which fabrics can you use?", "¿Qué telas pueden usar?"),
  ("We run Lenzing modal, mulberry silk, Supima cotton, lyocell-modal rib, nylon ice silk, PLA fiber, combed cotton and brushed cashmere blends every week. Other blends, weights and finishes are available on request.",
   "Trabajamos cada semana modal Lenzing, seda de morera, algodón Supima, rib de lyocell-modal, nailon ice silk, fibra PLA, algodón peinado y mezclas perchadas con cachemira. Otras mezclas, gramajes y acabados están disponibles a pedido.")),
 (("Are the fabrics certified?", "¿Las telas están certificadas?"),
  ("Our fabric mill, Zhongshan Ronghai Knitting Co., Ltd., holds OEKO-TEX STANDARD 100 certificate 2601022 in Product Class I, the strictest class, valid until 31 January 2027. The garment factory passed an amfori BSCI social audit by Bureau Veritas in October 2026. Copies are sent on request.",
   "Nuestra tejeduría, Zhongshan Ronghai Knitting Co., Ltd., tiene el certificado OEKO-TEX STANDARD 100 n.º 2601022 en la Clase de producto I, la más exigente, válido hasta el 31 de enero de 2027. La fábrica de prendas aprobó una auditoría social amfori BSCI de Bureau Veritas en octubre de 2026. Enviamos copias a pedido.")),
 (("How do you control quality?", "¿Cómo controlan la calidad?"),
  ("Three QC teams cover cutting, sewing and finishing, and every order goes through three inspection rounds, with final inspection at AQL 2.5. We check goods against your approved sample before shipment, and third-party inspection is welcome.",
   "Tres equipos de control de calidad cubren corte, confección y acabado, y cada pedido pasa por tres rondas de inspección, con inspección final AQL 2.5. Revisamos la mercadería contra su muestra aprobada antes del embarque y se aceptan inspecciones de terceros.")),
 (("Do you ship to Latin America, the US and Europe?", "¿Envían a Latinoamérica, Estados Unidos y Europa?"),
  ("Yes. Cartons are packed to your list and shipped by sea or air from South China on FOB or CIF terms. We book freight and prepare the export documents and customs paperwork.",
   "Sí. Las cajas se empacan según su lista y se embarcan por vía marítima o aérea desde el sur de China en términos FOB o CIF. Reservamos el flete y preparamos los documentos de exportación y los trámites aduaneros.")),
]

# ---------------------------------------------------------------- new Spanish text
ES_NEW = {
 "Men's":'Hombre', "Women's":'Mujer', 'Thermal':'Térmica', 'Factory':'Fábrica', 'FAQ':'Preguntas',
 'Home':'Inicio', 'Request a quote':'Solicitar cotización',
 'Shop by category':'Por categoría', 'Three product families, one factory.':'Tres familias de producto, una sola fábrica.',
 'Each category has its own base styles, fabrics and sizing. Open one to see every style we can brand for you.':'Cada categoría tiene sus propios modelos base, telas y tallas. Abra una para ver todos los modelos que podemos producir con su marca.',
 'Boxer briefs and trunks':'Bóxers', 'Briefs in silk, modal and cotton':'Calzones en seda, modal y algodón', 'Base layer sets':'Conjuntos de primera capa',
 'See the styles':'Ver los modelos', 'base styles':'modelos base',
 'Inside the factory':'Dentro de la fábrica', 'See every production stage':'Ver todas las etapas de producción',
 'What you can change':'Lo que puede cambiar', 'Make it yours.':'Hágalo suyo.',
 'Fabric and weight':'Tela y gramaje', 'Color and print':'Color y estampado', 'Waistband':'Elástico de cintura', 'Gusset and lining':'Entrepierna y forro', 'Size chart':'Tabla de tallas', 'Labels and packaging':'Etiquetas y empaque',
 'Any composition from our fabric library, or knitted to your spec.':'Cualquier composición de nuestro catálogo de telas, o tejida según su especificación.',
 'Lab dips to your Pantone references; all-over prints from your artwork.':'Lab dips según sus referencias Pantone; estampado total a partir de su diseño.',
 'Jacquard woven or printed with your logo, in your width and color.':'Jacquard tejido o estampado con su logo, en el ancho y color que elija.',
 'Silk, cotton, modal or PLA fiber, single or double layer.':'Seda, algodón, modal o fibra PLA, en capa simple o doble.',
 "Graded to your market's sizing: US, EU, LatAm or Asia.":'Escalada a las tallas de su mercado: EE. UU., Europa, Latinoamérica o Asia.',
 'Woven or heat-transfer labels, hang tags, bags and boxes.':'Etiquetas tejidas o transfer, etiquetas colgantes, bolsas y cajas.',
 'Questions about this category':'Preguntas sobre esta categoría', 'All questions':'Todas las preguntas',
 'Styles in this category':'Modelos de esta categoría',
 'Production stages':'Etapas de producción', 'Back to home':'Volver al inicio',
 'Page not found':'Página no encontrada', 'This page does not exist or has moved.':'Esta página no existe o se ha movido.', 'Go to the home page':'Ir a la página de inicio',
 'Send by email':'Enviar por correo', 'Pages':'Páginas', 'Contact':'Contacto',
 'Copy':'Copiar',
}
for (qe, qs), (ae, as_) in FAQ: ES_NEW[qe] = qs; ES_NEW[ae] = as_
for pg in PAGES:
    for k in ('title','desc','h1','intro'):
        if k in pg: ES_NEW[pg[k][0]] = pg[k][1]
for c, code, imgs, n, cp, tx in P:
    ES_NEW[n[0]] = n[1]; ES_NEW[cp[0]] = cp[1]; ES_NEW[tx[0]] = tx[1]

base = json.load(open(os.path.join(SRC, 'es_base.json')))
ES = dict(base['T']); ES.update(ES_NEW)
ES_ATTR = dict(base['PH'])
ES_ATTR.update({
 'Language':'Idioma', 'Sections':'Secciones', 'Lion Fashion home':'Inicio de Lion Fashion', 'Production summary':'Resumen de producción',
})

# ---------------------------------------------------------------- helpers
def url(lang, slug):
    p = ('/es/' if lang == 'es' else '/') + (slug + '/' if slug else '')
    return p
def absu(lang, slug): return SITE + url(lang, slug)
def esc(s): return html.escape(s, quote=True)

SECT = open(os.path.join(SRC, 'sections.html')).read()
def section(sid):
    m = re.search(r'(<section class="block" id="%s">.*?\n  </section>)' % sid, SECT, re.S)
    return m.group(1)
def chunk(start, end):
    i = SECT.index(start); j = SECT.index(end, i) + len(end)
    return SECT[i:j]

def card(p):
    c, code, imgs, n, cp, tx = p
    sw = ''
    if len(imgs) > 1:
        sw = '<div class="swatches">' + ''.join(
            f'<button class="sw" type="button" aria-label="Colorway {j+1}" aria-pressed="{"true" if j==0 else "false"}" data-m="{m}"><img src="/img/{m}.jpg?v={IMGV}" alt="" loading="lazy" width="640" height="640"></button>'
            for j, m in enumerate(imgs)) + '</div>'
    return (f'<article class="card" data-c="{c}"><div class="plate"><img src="/img/{imgs[0]}.jpg?v={IMGV}" alt="{esc(n[0])}" loading="lazy" width="640" height="640">'
            f'<span class="hole">{code}</span></div><div class="body"><h3>{esc(n[0])}</h3><div class="comp">{esc(cp[0])}</div><p>{esc(tx[0])}</p>{sw}</div></article>')

def header(slug):
    links = ''.join(f'<a href="/{p["slug"]}/"{" aria-current=\"page\"" if p["slug"]==slug else ""}>{esc(p["nav"][0])}</a>' for p in PAGES if p['nav'])
    return f'''<header class="top">
  <div class="wrap">
    <a class="mark" href="/" aria-label="Lion Fashion home"><span class="lf" aria-hidden="true"><span>L<span class="f">F</span></span></span><b>LION FASHION</b><span>UNDERWEAR OEM · ODM</span></a>
    <nav class="links" aria-label="Sections">{links}</nav>
    <div class="lang" aria-label="Language"><a href="@@EN@@" hreflang="en" data-l="en">EN</a><a href="@@ES@@" hreflang="es" data-l="es">ES</a></div>
    <a class="btn" href="#contact">Request a quote</a>
  </div>
</header>'''

def footer():
    links = ''.join(f'<a href="/{p["slug"]}/">{esc(p["nav"][0])}</a>' for p in PAGES if p['nav'])
    return f'''<footer>
  <div class="wrap">
    <div class="fcol"><span class="lf" aria-hidden="true"><span>L<span class="f">F</span></span></span><p><b>Shanghai Lion Industry Co., Ltd.</b> · 上海涞沅实业有限公司 · Underwear OEM / ODM</p><p>Production in Zhongshan, Guangdong, China</p></div>
    <nav class="fnav" aria-label="Pages"><a href="/">Home</a>{links}</nav>
    <div class="fcol"><p class="mono">{EMAIL}</p><p class="mono">WhatsApp {WA}</p></div>
  </div>
</footer>'''

def crumbs(pg):
    if not pg['slug']: return ''
    return f'<nav class="crumbs wrap" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>{esc(pg["nav"][0])}</span></nav>'

def page_head(pg):
    return f'''<section class="phead">
  <div class="wrap phead-grid">
    <div>
      <h1>{esc(pg["h1"][0])}</h1>
      <p class="lede">{esc(pg["intro"][0])}</p>
    </div>
    {f'<img src="/img/{pg["img"]}" alt="" width="1400" height="652">' if pg.get("img") else ''}
  </div>
</section>'''

CUSTOM = [('Fabric and weight','Any composition from our fabric library, or knitted to your spec.'),
          ('Color and print','Lab dips to your Pantone references; all-over prints from your artwork.'),
          ('Waistband','Jacquard woven or printed with your logo, in your width and color.'),
          ('Gusset and lining','Silk, cotton, modal or PLA fiber, single or double layer.'),
          ('Size chart',"Graded to your market's sizing: US, EU, LatAm or Asia."),
          ('Labels and packaging','Woven or heat-transfer labels, hang tags, bags and boxes.')]

def faq_html(items, heading=None, more=False):
    qs = ''.join(f'<details class="qa"><summary><h3>{esc(q[0])}</h3></summary><p>{esc(a[0])}</p></details>' for q, a in items)
    h = f'<div class="head"><div><h2>{esc(heading)}</h2></div></div>' if heading else ''
    m = '<p class="note"><a href="/faq/">All questions</a></p>' if more else ''
    return f'<section class="block" id="faq"><div class="wrap">{h}<div class="faqs">{qs}</div>{m}</div></section>'

CAT_FAQ = {'men': [0, 1, 4], 'women': [5, 6, 4], 'thermal': [2, 0, 8]}

def body_for(pg):
    s = pg['slug']
    if s == '':
        cats = ''
        for slug, cat, h3, pic in [('mens-underwear-manufacturer','men','Boxer briefs and trunks','m-seamless-black'),
                                   ('womens-underwear-manufacturer','women','Briefs in silk, modal and cotton','w-silk-taupe'),
                                   ('thermal-underwear-manufacturer','thermal','Base layer sets','t-men-cotton')]:
            n = sum(1 for p in P if p[0] == cat)
            nav = next(p['nav'][0] for p in PAGES if p['slug'] == slug)
            cats += (f'<a class="catcard" href="/{slug}/"><span class="plate"><img src="/img/{pic}.jpg" alt="" loading="lazy" width="640" height="640"></span>'
                     f'<span class="cbody"><span class="eyebrow">{esc(nav)}</span><h3>{esc(h3)}</h3><span class="cmeta"><span class="mono">{n}</span> <span>base styles</span></span><span class="go">See the styles</span></span></a>')
        catsec = f'''<section class="block" id="categories"><div class="wrap">
  <div class="head"><div><p class="eyebrow">Shop by category</p><h2>Three product families, one factory.</h2></div><p class="lede">Each category has its own base styles, fabrics and sizing. Open one to see every style we can brand for you.</p></div>
  <div class="cats">{cats}</div>
</div></section>'''
        teaser = '''<section class="block" id="factory-teaser"><div class="wrap">
  <div class="head"><div><p class="eyebrow">Inside the factory</p><h2>One supply chain, seven stages, under one roof.</h2></div><p class="lede">Fabric, trims and garments are made inside the same group. That keeps cost down, keeps fabric traceable to the lot, and means a delay in one department is visible to the next.</p></div>
  <div class="teaser"><img src="/img/f-creel.jpg" alt="Long creel of white yarn cones feeding circular knitting machines" loading="lazy" width="1400" height="435"><img src="/img/f-line.jpg" alt="Rows of sewing operators with an overhead hanging line of blue totes" loading="lazy" width="1400" height="652"><img src="/img/f-cutting.jpg" alt="Automatic cutting table cutting nested underwear pattern pieces" loading="lazy" width="1400" height="816"></div>
  <p class="note"><a class="btn ghost" href="/factory/">See every production stage</a></p>
</div></section>'''
        return (chunk('<section class="hero">', '</section>') + '\n' + chunk('<div class="figures">', '</p></div>')
                + '\n' + section('programs') + '\n' + catsec + '\n' + teaser + '\n' + section('process') + '\n' + section('compliance'))
    if s == 'factory':
        chain = section('factory')
        chain = re.sub(r'<div class="head">.*?<p class="lede">.*?</p>\s*</div>', '', chain, count=1, flags=re.S)  # page head replaces it
        return page_head(pg) + '\n' + chain + '\n' + section('materials') + '\n' + section('compliance')
    if s == 'faq':
        return page_head(pg) + '\n' + faq_html(FAQ)
    cat = pg['cat']
    cards = ''.join(card(p) for p in P if p[0] == cat)
    cust = ''.join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in CUSTOM)
    return (page_head(pg) + f'''
<section class="block" id="styles"><div class="wrap">
  <div class="head"><div><p class="eyebrow">ODM style library</p><h2>Styles in this category</h2></div><p class="lede">A selection from the current library. Each base can change fabric, color, waistband and packaging. Select a color dot to see another colorway.</p></div>
  <div class="grid{' g3' if sum(1 for p in P if p[0] == cat) % 3 == 0 else ''}">{cards}</div>
  <p class="note">Product photos show developed samples. Retail claims such as antibacterial grades depend on the final fabric and finish and are confirmed by test report for your order.</p>
</div></section>
<section class="block" id="custom"><div class="wrap">
  <div class="head"><div><p class="eyebrow">What you can change</p><h2>Make it yours.</h2></div></div>
  <div class="custom">{cust}</div>
</div></section>
''' + faq_html([FAQ[i] for i in CAT_FAQ[cat]], 'Questions about this category', more=True) + '\n' + section('programs'))

# ---------------------------------------------------------------- structured data
ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "Lion Fashion", "legalName": "Shanghai Lion Industry Co., Ltd.",
       "alternateName": ["Lion Fashion Underwear", "Shanghai Lion Industry", "上海涞沅实业有限公司"],
       "url": SITE + "/", "logo": SITE + "/img/logo.png", "email": EMAIL, "telephone": "+1-314-250-8276",
       "address": {"@type": "PostalAddress", "addressLocality": "Shanghai", "addressCountry": "CN"},
       "areaServed": ["Latin America", "Mexico", "United States", "Europe", "Asia"], "knowsLanguage": ["en", "es"]}

def ld(pg, lang):
    i = 0 if lang == 'en' else 1
    g = [ORG] if pg['slug'] == '' else [{"@type": "Organization", "@id": SITE + "/#org", "name": "Lion Fashion", "url": SITE + "/"}]
    g.append({"@type": "WebPage", "@id": absu(lang, pg['slug']) + "#page", "url": absu(lang, pg['slug']), "name": pg['title'][i],
              "description": pg['desc'][i], "inLanguage": lang, "isPartOf": {"@type": "WebSite", "name": "Lion Fashion", "url": SITE + "/"},
              "publisher": {"@id": SITE + "/#org"}})
    if pg['slug']:
        g.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home" if lang == 'en' else "Inicio", "item": absu(lang, '')},
            {"@type": "ListItem", "position": 2, "name": pg['nav'][i], "item": absu(lang, pg['slug'])}]})
    items = None
    if pg['slug'] == 'faq': items = FAQ
    elif pg.get('cat'): items = [FAQ[k] for k in CAT_FAQ[pg['cat']]]
    if items:
        g.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q[i], "acceptedAnswer": {"@type": "Answer", "text": a[i]}} for q, a in items]})
    if pg.get('cat'):
        g.append({"@type": "ItemList", "name": pg['h1'][i], "itemListElement": [
            {"@type": "ListItem", "position": k + 1, "name": p[3][i], "description": p[5][i], "image": SITE + f"/img/{p[2][0]}.jpg"}
            for k, p in enumerate([p for p in P if p[0] == pg['cat']])]})
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False)

# ---------------------------------------------------------------- page assembly
def render(pg, lang):
    i = 0 if lang == 'en' else 1
    s = pg['slug']
    og_img = SITE + '/img/' + (pg.get('img') or 'f-hanging.jpg')
    head = f'''<!doctype html>
<html lang="{lang}" data-brand="champagne">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(pg["title"][i])}</title>
<meta name="description" content="{esc(pg["desc"][i])}">
<link rel="canonical" href="{absu(lang, s)}">
<link rel="alternate" hreflang="en" href="{absu('en', s)}">
<link rel="alternate" hreflang="es" href="{absu('es', s)}">
<link rel="alternate" hreflang="x-default" href="{absu('en', s)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lion Fashion">
<meta property="og:locale" content="{'en_US' if lang=='en' else 'es_419'}">
<meta property="og:title" content="{esc(pg["title"][i])}">
<meta property="og:description" content="{esc(pg["desc"][i])}">
<meta property="og:url" content="{absu(lang, s)}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1E1D21">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" href="/img/favicon.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<script type="application/ld+json">{ld(pg, lang)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/site.css?v=@@V@@">
</head>
<body>'''
    body = (header(s) + '\n<main id="top">\n' + crumbs(pg) + '\n' + body_for(pg) + '\n' + section('contact') + '\n</main>\n' + footer()
            + '\n<script src="/assets/site.js?v=@@V@@" defer></script>\n</body>\n</html>\n')
    # links inside sections that pointed at one-page anchors
    body = body.replace('href="#catalog"', 'href="/mens-underwear-manufacturer/"')
    body = body.replace('src="img/', 'src="/img/')
    body = body.replace('<button class="btn ghost" type="button" id="copy-txt">', f'<a class="btn ghost" id="mail-link" href="mailto:{EMAIL}">Send by email</a><button class="btn ghost" type="button" id="copy-txt">')
    body = body.replace('<a class="btn ghost" href="#catalog">Browse ODM styles</a>', '<a class="btn ghost" href="/mens-underwear-manufacturer/">Browse ODM styles</a>')
    if lang == 'es':
        body = translate(body)
        body = re.sub(r'href="/(?!/|img/|assets/|favicon)', 'href="/es/', body)
        body = re.sub(r'aria-label="Colorway (\d)"', r'aria-label="Color \1"', body)
    body = body.replace('@@EN@@', url('en', s)).replace('@@ES@@', url('es', s))
    body = body.replace(f'data-l="{lang}"', f'data-l="{lang}" aria-current="true"')
    return head + '\n' + body

MISSING = []
def translate(h):
    keys = sorted(ES, key=len, reverse=True)
    for k in keys:
        h = h.replace('>' + k + '<', '>' + ES[k] + '<')
        for ek in {esc(k), esc(k).replace('&#x27;', "'")}:
            if ek != k: h = h.replace('>' + ek + '<', '>' + esc(ES[k]).replace('&#x27;', "'").replace('&quot;', '"') + '<')
    for k, v in ES_ATTR.items():
        h = h.replace(f'="{k}"', f'="{v}"')
    # alt text for product cards
    for c, code, imgs, n, cp, tx in P:
        h = h.replace(f'alt="{esc(n[0])}"', f'alt="{esc(n[1])}"')
    # report leftovers
    for t in re.findall(r'>([^<>]*[A-Za-z][^<>]*)<', h):
        t2 = t.strip()
        if re.search(r"\b(the|and|your|our|with|for|of|to)\b", t2) and t2 not in MISSING:
            MISSING.append(t2)
    return h

def main():
    if os.path.isdir(OUT):
        for name in os.listdir(OUT):
            if name in ('img', 'assets', 'favicon.svg'): continue
            pth = os.path.join(OUT, name)
            shutil.rmtree(pth) if os.path.isdir(pth) else os.remove(pth)
    v = TODAY.replace('-', '')
    for pg in PAGES:
        for lang in ('en', 'es'):
            d = os.path.join(OUT, *(['es'] if lang == 'es' else []), *( [pg['slug']] if pg['slug'] else []))
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w').write(render(pg, lang).replace('@@V@@', v))
    # 404
    nf = f'''<!doctype html><html lang="en" data-brand="champagne"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found | Lion Fashion</title><meta name="robots" content="noindex"><link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Hanken+Grotesk:wght@400;600&display=swap"><link rel="stylesheet" href="/assets/site.css?v={v}"></head>
<body>{header("").replace("@@EN@@", "/").replace("@@ES@@", "/es/").replace('href="#contact"', 'href="/#contact"')}<main class="wrap nf"><p class="eyebrow">404</p><h1>Page not found</h1><p class="lede">This page does not exist or has moved.</p><p><a class="btn" href="/">Go to the home page</a> <a class="btn ghost" href="/es/">Español</a></p></main>{footer()}</body></html>'''
    open(os.path.join(OUT, '404.html'), 'w').write(nf)
    # sitemap + robots
    rows = []
    for pg in PAGES:
        alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{absu(l2, pg["slug"])}"/>' for l, l2 in (('en','en'),('es','es'),('x-default','en')))
        for lang in ('en', 'es'):
            rows.append(f'  <url><loc>{absu(lang, pg["slug"])}</loc><lastmod>{TODAY}</lastmod>{alts}</url>')
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(rows) + '\n</urlset>\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    # wrangler config follows the domain
    open(os.path.join(ROOT, 'wrangler.jsonc'), 'w').write(json.dumps({
        "name": "lionfashion", "main": "src/worker.js", "compatibility_date": "2026-09-01", "workers_dev": True, "preview_urls": False,
        "routes": [{"pattern": DOMAIN, "custom_domain": True}, {"pattern": "www." + DOMAIN, "custom_domain": True}],
        "vars": {"HOME": DOMAIN},
        "assets": {"directory": "./public", "binding": "ASSETS", "run_worker_first": True, "html_handling": "auto-trailing-slash", "not_found_handling": "404-page"}
    }, indent=2) + '\n')
    if MISSING:
        print('Untranslated English text in Spanish pages:'); [print('  -', m) for m in MISSING]; sys.exit(1)
    print(f'Built {len(PAGES)*2} pages for {SITE}')

if __name__ == '__main__':
    main()

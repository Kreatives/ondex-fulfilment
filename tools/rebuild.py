#!/usr/bin/env python3
"""Unified rebuild: genereert contact.html + de 6 subpagina's uit index.html
(de shell). Draai vanuit de projectroot:  python3 tools/rebuild.py
Daarna ALTIJD:  bash tools/check-all-pages.sh

Zo blijven header/footer/widget/fonts/stijl van ALLE pagina's identiek aan de
homepage. Nooit losse pagina's handmatig patchen -> altijd via dit script.
"""
import re, sys, subprocess, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); sys.path.insert(0,os.path.join(ROOT,'tools'))
from scope_css import scope_css as scope

idx=open('index.html',encoding='utf-8').read()
site_src=open('assets/css/site.css').read().replace('hero-actions','sa-actions')
site_scoped=scope(site_src,'main')

OVERRIDES=r"""
/* === Ondex consistent designsysteem: content exact in homepage-stijl === */
html body main .page-hero h1{font-size:clamp(44px,4.6vw,66px)!important;font-weight:850!important;letter-spacing:-.05em!important;line-height:1.02!important;}
html body main h2{font-size:clamp(30px,3vw,44px)!important;font-weight:800!important;letter-spacing:-.04em!important;line-height:1.06!important;}
html body main h3{font-size:clamp(20px,1.5vw,23px)!important;font-weight:750!important;letter-spacing:-.02em!important;line-height:1.2!important;}
html body main p{font-size:16px!important;line-height:1.7!important;}
html body main .lead{font-size:18px!important;line-height:1.65!important;}
html body main .btn{min-height:52px!important;padding:0 24px!important;border-radius:999px!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;gap:10px!important;font-size:14px!important;font-weight:800!important;letter-spacing:-.01em!important;line-height:1!important;width:auto!important;}
html body main .btn-primary,html body main .btn-blue,html body main .quote{background:#08B6C6!important;color:#fff!important;border:0!important;}
html body main .btn-primary:hover,html body main .btn-blue:hover,html body main .quote:hover{background:#079EAD!important;}
html body main .container{width:min(1240px,calc(100% - 48px))!important;margin-inline:auto!important;}
@media(min-width:1300px){html body main .container{width:min(1440px,calc(100% - 64px))!important;}}
/* Highlights in koppen: merk-cyaan op licht, helder op donker */
html body main .page-hero h1 span{color:#08B6C6!important;}
html body main .page-hero--image h1 span{color:#4bdde7!important;}
/* Eyebrow-pills consistent met homepage: cyaan tekst op licht-cyaan pill */
html body main .pill-label{background:#eafbfc!important;color:#079ead!important;}
html body main .page-hero--image .pill-label{background:rgba(255,255,255,.15)!important;color:#fff!important;}
/* WCAG: koppen op donkere content-secties leesbaar wit, accent helder cyaan */
html body main .mp-section h2,html body main .mp-section h3,html body main .person-band__body h2,html body main .person-band__body h3,html body main .showcase-head h2,html body main .showcase h3,html body main .cta-band h2,html body main .cta-band h3{color:#fff!important;}
html body main .mp-section .eyebrow{color:#4bdde7!important;}
html body main .showcase-head h2 span,html body main .cta-band h2 span{color:#4bdde7!important;}
html body main .cta-band p{color:#b2bdc1!important;}
/* Scroll-reveal animaties (fade + slide-up); alleen met JS, geen flash */
html.reveal-on body main [data-reveal]{opacity:0;transform:translateY(26px);transition:opacity .75s cubic-bezier(.16,1,.3,1),transform .75s cubic-bezier(.16,1,.3,1);will-change:opacity,transform;}
html.reveal-on body main [data-reveal].is-visible{opacity:1;transform:none;}
/* Kaart-grids: wave/golf — gestaggerd inschuiven */
html.reveal-on body main [data-reveal] .showcase-grid>*,html.reveal-on body main [data-reveal] .mp-grid>*,html.reveal-on body main [data-reveal] .eco>*{opacity:0;transform:translateY(26px);transition:opacity .6s ease,transform .72s cubic-bezier(.16,1,.3,1);}
html.reveal-on body main [data-reveal].is-visible .showcase-grid>*,html.reveal-on body main [data-reveal].is-visible .mp-grid>*,html.reveal-on body main [data-reveal].is-visible .eco>*{opacity:1;transform:none;}
html.reveal-on body main [data-reveal].is-visible .showcase-grid>*:nth-child(1),html.reveal-on body main [data-reveal].is-visible .mp-grid>*:nth-child(1),html.reveal-on body main [data-reveal].is-visible .eco>*:nth-child(1){transition-delay:.16s;}
html.reveal-on body main [data-reveal].is-visible .showcase-grid>*:nth-child(2),html.reveal-on body main [data-reveal].is-visible .mp-grid>*:nth-child(2),html.reveal-on body main [data-reveal].is-visible .eco>*:nth-child(2){transition-delay:.28s;}
html.reveal-on body main [data-reveal].is-visible .showcase-grid>*:nth-child(3),html.reveal-on body main [data-reveal].is-visible .mp-grid>*:nth-child(3),html.reveal-on body main [data-reveal].is-visible .eco>*:nth-child(3){transition-delay:.40s;}
html.reveal-on body main [data-reveal].is-visible .showcase-grid>*:nth-child(4),html.reveal-on body main [data-reveal].is-visible .eco>*:nth-child(4){transition-delay:.52s;}
@media(prefers-reduced-motion:reduce){html.reveal-on body main [data-reveal],html.reveal-on body main [data-reveal] .showcase-grid>*,html.reveal-on body main [data-reveal] .mp-grid>*,html.reveal-on body main [data-reveal] .eco>*{opacity:1!important;transform:none!important;transition:none!important;}}
"""

HERO={
 'integraties.html':('<h1>Koppel je kanalen, wij regelen de logistiek erachter.</h1>','<h1>Koppel je kanalen, <span>wij regelen de logistiek erachter.</span></h1>'),
 'over-ondex.html':('<h1>Logistiek zonder kopzorgen, met een mens aan de lijn.</h1>','<h1>Logistiek zonder kopzorgen, <span>met een mens aan de lijn.</span></h1>'),
 'tarieven.html':('<h1>Eerlijke all-in tarieven, zonder verrassingen achteraf.</h1>','<h1>Eerlijke all-in tarieven, <span>zonder verrassingen achteraf.</span></h1>'),
 'diensten.html':('<h1>Je complete logistieke afdeling, onder één dak.</h1>','<h1>Je complete logistieke afdeling, <span>onder één dak.</span></h1>'),
 'marketplace-fulfilment.html':('<h1>Verkoop op elke marketplace, wij regelen de logistiek.</h1>','<h1>Verkoop op elke marketplace, <span>wij regelen de logistiek.</span></h1>'),
 'webshop-fulfilment.html':('<h1>Fulfilment die je webshop laat groeien.</h1>','<h1>Fulfilment die <span>je webshop laat groeien.</span></h1>'),
}
NAV={'integraties.html':'<a href="/integraties">Integraties</a>','tarieven.html':'<a href="/tarieven">Tarieven</a>','over-ondex.html':'<a href="/over-ondex">Over Ondex</a>','diensten.html':None,'marketplace-fulfilment.html':'<a href="/marketplace-fulfilment">Fulfilment voor marketplaces<small>Bol.com, TikTok Shop, Amazon en meer.</small></a>','webshop-fulfilment.html':'<a href="/webshop-fulfilment">Fulfilment voor webshops<small>Opslag, pick &amp; pack, verzending en retouren.</small></a>'}

def head_show(p): return subprocess.run(['git','show',f'HEAD:{p}'],capture_output=True,text=True).stdout

def build(title,desc,main_html,head_styles,extra_scripts,nav_link):
    out=idx
    vp='<meta name="viewport" content="width=device-width,initial-scale=1">\n'
    out=out.replace(vp, vp+f'<title>{title}</title>\n<meta name="description" content="{desc}">\n',1)
    out=out.replace('<body class="ondex home">','<body class="ondex">',1)
    out=out.replace('</head>', head_styles+'\n</head>',1)
    out=re.sub(r'<main[^>]*>.*?</main>', lambda m:main_html, out, count=1, flags=re.DOTALL)
    out=out.replace('<a class="logo" href="#top">','<a class="logo" href="/">',1)
    out=out.replace('<a class="footer-logo" href="#top" aria-label="Ondex Fulfilment">','<a class="footer-logo" href="/" aria-label="Ondex Fulfilment">',1)
    out=out.replace('href="#marketplace-partners"','href="/#marketplace-partners"',3)
    out=out.replace('href="#integraties"','href="/#integraties"',1).replace('href="#werkwijze"','href="/#werkwijze"',1).replace('href="#faq"','href="/#faq"',1)
    if nav_link and nav_link in out:
        out=out.replace(nav_link, nav_link.replace('<a href=','<a aria-current="page" href=',1),1)
    if extra_scripts:
        out=out.replace('</body>', extra_scripts+'\n</body>',1)
    return out

# ---- subpagina's ----
sub_styles='<style id="ondex-standalone-css">\n'+site_scoped+'\n'+OVERRIDES+'\n</style>'
for page in HERO:
    src=head_show(page)
    cm=re.search(r'<main[^>]*>.*?</main>',src,re.DOTALL).group(0); cm=re.sub(r'^<main[^>]*>','<main>',cm); cm=cm.replace('hero-actions','sa-actions')
    old,new=HERO[page]; cm=cm.replace(old,new,1)
    title=re.search(r'<title>(.*?)</title>',src,re.DOTALL).group(1); dm=re.search(r'<meta name="description" content="(.*?)">',src,re.DOTALL); desc=dm.group(1) if dm else ''
    open(page,'w',encoding='utf-8').write(build(title,desc,cm,sub_styles,'',NAV[page]))
    print("built",page)

# ---- contact: haal unieke onderdelen uit de HUIDIGE contact.html ----
c=open('contact.html',encoding='utf-8').read()
def grab(pat): m=re.search(pat,c,re.DOTALL); return m.group(0) if m else ''
contact_main=grab(r'<main class="cl-page">.*?</main>')
contact_css=grab(r'<style id="ondex-contact-css">.*?</style>')+'\n'+grab(r'<style id="ondex-contact-maxwidth-fix">.*?</style>')+'\n'+grab(r'<style id="ondex-contact-widget-fix">.*?</style>')
contact_form=''
for fm in re.findall(r'<script>\(function\(\)\{.*?\}\)\(\);</script>', c, re.DOTALL):
    if 'ondex-offerte-form' in fm: contact_form=fm; break
assert contact_main and contact_css and contact_form, "contact-onderdelen niet gevonden"
open('contact.html','w',encoding='utf-8').write(build(
  'Contact & offerte aanvragen | Ondex Fulfilment',
  'Vraag vrijblijvend een fulfilmentofferte aan bij Ondex. Deel je volumes en verkoopkanalen en ontvang binnen 24 uur een persoonlijk voorstel.',
  contact_main, contact_css, contact_form, '<a href="/contact">Contact</a>'))
print("built contact.html")
print("\nKLAAR. Draai nu: bash tools/check-all-pages.sh")

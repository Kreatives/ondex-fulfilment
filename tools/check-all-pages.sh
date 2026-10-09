#!/usr/bin/env bash
# Rendert ALLE pagina's headless en rapporteert (near-)onzichtbare / laag-contrast
# tekst per pagina. Draai vanuit de projectroot:  bash tools/check-all-pages.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP="$(mktemp -d)"
ln -sfn "$ROOT/assets" "$TMP/assets"
[ -f "$ROOT/style.css" ] && ln -sfn "$ROOT/style.css" "$TMP/style.css"
CHECK_JS="$(cat "$ROOT/tools/contrast-check.js")"
PAGES="${*:-index contact integraties over-ondex tarieven diensten marketplace-fulfilment webshop-fulfilment}"
FAIL=0
for p in $PAGES; do
  [ -f "$ROOT/$p.html" ] || { echo "SKIP $p (bestaat niet)"; continue; }
  # inject checker + force all reveal-animaties zichtbaar zodat we de eindtoestand meten
  python3 - "$ROOT/$p.html" "$TMP/$p.html" "$CHECK_JS" <<'PY'
import sys
src,dst,js=sys.argv[1],sys.argv[2],sys.argv[3]
s=open(src,encoding='utf-8').read()
force='<style>html.reveal-on [data-reveal],html.reveal-on [data-reveal] *,.cl-benefits-panel *,[data-reveal]{opacity:1!important;transform:none!important;filter:none!important}</style>'
inj=force+'<script>window.addEventListener("load",function(){setTimeout(function(){'+js+'},700)})</script>'
s=s.replace('</body>',inj+'</body>',1)
open(dst,'w',encoding='utf-8').write(s)
PY
  OUT="$("$CHROME" --headless --disable-gpu --hide-scrollbars --virtual-time-budget=9000 --window-size=1680,1200 --dump-dom "file://$TMP/$p.html" 2>/dev/null | grep -o 'id="CONTRAST_REPORT" data-json="[^"]*"' || true)"
  JSON="$(python3 - "$OUT" <<'PY'
import sys,re,html
m=re.search(r'data-json="(.*)"',sys.argv[1] if len(sys.argv)>1 else '')
print(html.unescape(m.group(1)) if m else '[]')
PY
)"
  python3 - "$p" "$JSON" <<'PY'
import sys,json
page,js=sys.argv[1],sys.argv[2]
try: issues=json.loads(js)
except Exception: issues=[]
# harde bugs = onzichtbaar op een SOLID achtergrond (geen afbeelding eronder)
hard=[i for i in issues if i.get('severity')=='INVISIBLE' and not i.get('onImg')]
onimg=[i for i in issues if i.get('severity')=='INVISIBLE' and i.get('onImg')]
low=[i for i in issues if i.get('severity')=='low']
if not hard and not onimg and not low:
    print(f"\033[32m✓ {page:26s} schoon\033[0m"); sys.exit(0)
c='31' if hard else ('33' if onimg else '0')
print(f"\033[{c}m{'✗' if hard else '•'} {page:26s} {len(hard)} HARDE BUG, {len(onimg)} op-afbeelding (verify), {len(low)} laag-contrast\033[0m")
for i in hard[:14]:
    print(f"    \033[31mBUG\033[0m cr={i['cr']:<4} {i['tag']:<4} {i['fs']}px  \"{i['t']}\"  {i['color']} op {i['bg']}")
for i in onimg[:8]:
    print(f"    ~img cr={i['cr']:<4} {i['tag']:<4} {i['fs']}px  \"{i['t']}\"  {i['color']} (achtergrond=foto/gradient, handmatig checken)")
for i in low[:6]:
    print(f"    low  cr={i['cr']:<4}/{i['need']} {i['tag']:<4} {i['fs']}px  \"{i['t']}\"  {i['color']} op {i['bg']}")
PY
  [ -n "$JSON" ] && [ "$JSON" != "[]" ] && FAIL=1 || true
done
rm -rf "$TMP"
echo
[ "$FAIL" = "0" ] && echo "KLAAR: alle pagina's schoon." || echo "KLAAR: er zijn problemen (zie hierboven)."

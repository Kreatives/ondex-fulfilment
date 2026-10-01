#!/usr/bin/env python3
"""Rendert het WordPress-thema naar een statische index.html voor lokale preview."""
import re
from pathlib import Path

root = Path(__file__).parent

header = (root / "header.php").read_text(encoding="utf-8")
front = (root / "front-page.php").read_text(encoding="utf-8")

# get_header()/get_footer() strippen uit front-page
front = re.sub(r"<\?php\s+get_(header|footer)\(\);\s*\?>", "", front)

fonts = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap">'
    '<link rel="stylesheet" href="/style.css">'
)

repl = {
    r"<\?php\s+language_attributes\(\);\s*\?>": 'lang="nl-NL"',
    r"<\?php\s+bloginfo\('charset'\);\s*\?>": "UTF-8",
    r"<\?php\s+body_class\('ondex'\);\s*\?>": 'class="ondex home"',
    r"<\?php\s+wp_body_open\(\);\s*\?>": "",
    r"<\?php\s+wp_head\(\);\s*\?>": fonts,
    r"<\?php\s+echo\s+esc_url\(\s*get_template_directory_uri\(\)\s*\);\s*\?>": "",
}

for pat, val in repl.items():
    header = re.sub(pat, val, header)

# template-dir uri komt ook in front-page voor
tpl = r"<\?php\s+echo\s+esc_url\(\s*get_template_directory_uri\(\)\s*\);\s*\?>"
front = re.sub(tpl, "", front)

# home_url( '/pad/' ) -> /pad/
home_url = re.compile(
    r"<\?php\s+echo\s+esc_url\(\s*home_url\(\s*'([^']*)'\s*\)\s*\);\s*\?>"
)
header = home_url.sub(lambda m: m.group(1), header)
front = home_url.sub(lambda m: m.group(1), front)

html = header + front + "\n</body>\n</html>\n"

# eventueel achtergebleven php-tags loggen
leftover = re.findall(r"<\?php.*?\?>", html, re.S)
if leftover:
    print(f"WAARSCHUWING: {len(leftover)} php-tag(s) niet vervangen:")
    for t in leftover[:10]:
        print("  ", t[:80].replace("\n", " "))

(root / "index.html").write_text(html, encoding="utf-8")
print(f"index.html geschreven ({len(html)} bytes)")

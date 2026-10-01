#!/usr/bin/env python3
"""Extraheert alle footer-gerelateerde CSS uit index.html naar assets/css/footer.css.

Pakt elke top-level regel waarvan de selector een footer-token bevat, behoudt
@media-wrappers (alleen met de relevante binnenregels) en voegt @keyframes toe die
door die regels worden aangeroepen. Helper-classes die alleen in de footer voorkomen
(contact-social, social-*, fill-dot, ondex-address-13, ondex-offerte-note) worden
meegenomen; die komen nergens anders op de subpagina's voor.
"""
import re
from pathlib import Path

root = Path(__file__).parent
html = (root / "index.html").read_text(encoding="utf-8")

# Alle <style>-inhoud samenvoegen
styles = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))

TOKENS = (
    "footer", "contact-social", "fill-dot", "ondex-address-13",
    "ondex-offerte-note", "social-linkedin", "social-instagram",
    "social-facebook", "social-tiktok",
)

def wants(selector: str) -> bool:
    s = selector.lower()
    return any(t in s for t in TOKENS)

def split_top_level(css: str):
    """Yield (prelude, body, kind) voor elk top-level blok."""
    i, n = 0, len(css)
    buf = []
    while i < n:
        ch = css[i]
        if ch == "{":
            prelude = "".join(buf).strip()
            depth, j = 1, i + 1
            while j < n and depth:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                j += 1
            body = css[i + 1:j - 1]
            kind = "at" if prelude.startswith("@") else "rule"
            yield prelude, body, kind
            buf = []
            i = j
        else:
            buf.append(ch)
            i += 1

kept = []            # lijst van (prelude, body) in originele volgorde
keyframes = {}       # naam -> volledige @keyframes-tekst
used_anim = set()

ANIM_RE = re.compile(r"animation(?:-name)?\s*:\s*([^;]+);", re.I)

def collect_anim(body: str):
    for m in ANIM_RE.finditer(body):
        for part in m.group(1).split(","):
            for tok in part.strip().split():
                # eerste niet-numerieke/niet-timing token is doorgaans de naam
                if re.match(r"^[A-Za-z_-][\w-]*$", tok) and tok.lower() not in (
                    "ease", "linear", "infinite", "alternate", "both", "forwards",
                    "backwards", "normal", "reverse", "ease-in", "ease-out",
                    "ease-in-out", "running", "paused", "none",
                ):
                    used_anim.add(tok)

for prelude, body, kind in split_top_level(styles):
    if kind == "rule":
        if wants(prelude):
            kept.append((prelude, body))
            collect_anim(body)
    elif prelude.lower().startswith("@keyframes"):
        name = prelude.split(None, 1)[1].strip() if " " in prelude else ""
        keyframes[name] = f"{prelude}{{{body}}}"
    elif prelude.lower().startswith("@media") or prelude.lower().startswith("@supports"):
        inner = [(p, b) for p, b, k in split_top_level(body) if k == "rule" and wants(p)]
        if inner:
            inner_css = "\n".join(f"  {p}{{{b.strip()}}}" for p, b in inner)
            kept.append((prelude, "\n" + inner_css + "\n"))
            for _, b in inner:
                collect_anim(b)

# Keyframes die daadwerkelijk gebruikt worden
anim_css = "\n".join(keyframes[n] for n in used_anim if n in keyframes)

out = [
    "/* Footer-styling, geextraheerd uit index.html zodat alle pagina's dezelfde footer tonen. */",
    ':root{--brand:#08B6C6;--ondex-kicker-font:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}\n',
]
for prelude, body in kept:
    if prelude.startswith("@"):
        out.append(f"{prelude}{{{body}}}")
    else:
        out.append(f"{prelude}{{{body.strip()}}}")
if anim_css:
    out.append("\n/* Gebruikte keyframes */")
    out.append(anim_css)

(root / "assets/css/footer.css").write_text("\n".join(out) + "\n", encoding="utf-8")

print(f"footer.css: {len(kept)} regels/blokken, {len([n for n in used_anim if n in keyframes])} keyframes")
print("Animaties gebruikt:", sorted(n for n in used_anim if n in keyframes))
# var() check
vars_used = sorted(set(re.findall(r"var\((--[\w-]+)", "\n".join(out))))
print("CSS-variabelen in footer.css:", vars_used)

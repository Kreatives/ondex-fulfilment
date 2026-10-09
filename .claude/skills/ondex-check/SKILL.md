---
name: ondex-check
description: >-
  Controleert ALLE pagina's van de Ondex Fulfilment-site in één keer op
  onzichtbare / laag-contrast tekst (WCAG) en op consistentie. Gebruik deze
  skill ALTIJD na elke visuele/CSS-wijziging aan de site, vóór committen/pushen,
  of wanneer de gebruiker vraagt "check alle pagina's", "zijn er zwarte teksten",
  "klopt het overal", of iets soortgelijks. Rendert elke pagina headless in
  Chrome en rapporteert per pagina de harde bugs.
---

# Ondex — alle pagina's checken

Doel: NOOIT meer "ik heb maar een paar pagina's gecheckt". Deze skill rendert
en controleert **elke** pagina (`index`, `contact`, `integraties`, `over-ondex`,
`tarieven`, `diensten`, `marketplace-fulfilment`, `webshop-fulfilment`).

## Stap 1 — draai de checker

```bash
bash tools/check-all-pages.sh
```

(Eén pagina checken: `bash tools/check-all-pages.sh over-ondex`.)

De checker rendert elke pagina met headless Chrome, forceert reveal-animaties
naar hun eindtoestand, en meet voor elk tekstelement het contrast t.o.v. de
**werkelijke** achtergrond (loopt door semi-transparante lagen, gradients en
glass/backdrop-filter heen).

## Stap 2 — lees de uitslag

Per pagina staat er: `<n> HARDE BUG, <n> op-afbeelding (verify), <n> laag-contrast`.

- **HARDE BUG** (rood) = tekst die (bijna) onzichtbaar is op een SOLID
  achtergrond (bijv. zwart op donker, wit op wit). **Dit MOET je fixen.**
  Het regelt de echte "waarom is dit zwart?"-problemen.
- **op-afbeelding (verify)** = witte tekst op een foto/gradient/glass. De
  checker kan de foto niet samplen; dit is meestal prima (hero-tekst, footer,
  glass-chips). Alleen handmatig checken als er net een foto/sectie is gewijzigd.
- **laag-contrast** = haalt de WCAG-norm net niet. Op deze site is dit
  grotendeels bewust: het merk-cyaan `#08B6C6` als accenttekst en witte tekst
  op cyaan knoppen (~2,47:1). Dat is een merkkeuze van de klant — niet als bug
  behandelen tenzij de klant er expliciet om vraagt.

**Groen vinkje / "0 HARDE BUG" op alle pagina's = klaar om te pushen.**

## Stap 3 — fix donkere-sectie-koppen

Komt er een HARDE BUG "zwart op donker" terug, dan zit er een donkere
content-container zonder witte kop. De fix hoort in de consistentie-laag
(`overrides` in de rebuild) — zie [[pages-on-homepage-shell]]. Donkere
containers op dit moment: `.showcase(-head)`, `.cta-band`, `.mp-section`,
`.person-band__body`. Voeg de nieuwe container daar toe met `color:#fff!important`
en het accent-span met `#4bdde7!important`, rebuild met de unified build, en
draai deze checker opnieuw tot alles 0 HARDE BUG is.

## Belangrijk

- De subpagina's én contact worden gegenereerd uit `index.html` (de shell) via
  de **unified rebuild**. Wijzig je de header/footer/widget/stijl in `index.html`,
  rebuild dan ALLE pagina's in één keer — anders loopt één pagina (vaak contact)
  uit de pas. Draai daarna altijd deze checker.
- Chrome-pad in het script: `/Applications/Google Chrome.app/...`. Geen Chrome =
  skill werkt niet; installeer Chrome of pas het pad aan.

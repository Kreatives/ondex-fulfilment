# Ondex Fulfilment

Website voor Ondex Fulfilment — webshop- en marketplace-fulfilment vanuit Didam.

## Opzet

Dit is een statische site. De pagina's staan als losse HTML-bestanden in de root, met
alle afbeeldingen, CSS, JS en fonts in `assets/`. Alle links en asset-verwijzingen zijn
relatief, dus de site werkt zowel lokaal als op GitHub Pages.

### Pagina's

| Bestand | Pagina |
| --- | --- |
| `index.html` | Homepage |
| `diensten.html` | Diensten |
| `webshop-fulfilment.html` | Webshop fulfilment |
| `marketplace-fulfilment.html` | Marketplace fulfilment |
| `integraties.html` | Integraties |
| `tarieven.html` | Tarieven |
| `over-ondex.html` | Over Ondex |
| `contact.html` | Contact |

## Lokaal bekijken

Open `index.html` direct in de browser, of start een lokale server:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Bron van de homepage

De homepage wordt gegenereerd uit het WordPress-thema (`header.php`, `front-page.php`)
via het buildscript:

```bash
python3 build_static.py
```

Dit rendert het thema naar `index.html` voor statische preview.

## Publiceren via GitHub Pages

1. Push deze repo naar GitHub.
2. Ga naar **Settings → Pages**.
3. Kies als source de branch `main` en map `/ (root)`.
4. De site staat live op de getoonde URL.

Het bestand `.nojekyll` zorgt dat GitHub Pages de bestanden ongewijzigd serveert.

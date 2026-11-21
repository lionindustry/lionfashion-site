# Lion Fashion website

Underwear OEM/ODM website of Lion Fashion, in English and Spanish.
All site files are in `public/`. Cloudflare Workers deploys this repository automatically on every change to `main`
.

## Pages

| English | Spanish |
|---|---|
| `/` home | `/es/` |
| `/mens-underwear-manufacturer/` | `/es/mens-underwear-manufacturer/` |
| `/womens-underwear-manufacturer/` | `/es/womens-underwear-manufacturer/` |
| `/thermal-underwear-manufacturer/` | `/es/thermal-underwear-manufacturer/` |
| `/factory/` | `/es/factory/` |
| `/faq/` | `/es/faq/` |

The pages are generated. Don't edit the HTML in `public/` by hand; edit the sources and rebuild:

    python3 tools/build.py

- `tools/build.py`: page list, titles and descriptions (EN/ES), product styles, FAQ, structured data, sitemap, robots, 404.
- `source/sections.html`: the English text of the shared sections (hero, programs, process, compliance, factory stages, fabrics, contact form).
- `source/es_base.json` and `ES_NEW` in `build.py`: Spanish translations. The build stops and lists any English text with no Spanish.
- `source/DOMAIN`: the site's domain (used for canonical links, hreflang, sitemap and `wrangler.jsonc`).
- `public/assets/site.css`, `public/assets/site.js`: styles (Champagne Noir theme) and the colorway dots / quote form.
- `public/img/`: photos, logo and icons.

## Search engines (SEO)

Each page has its own title, description, canonical link, `hreflang` links to its other language, share card,
and structured data (Organization, WebPage, BreadcrumbList; FAQPage on the FAQ and category pages; ItemList of styles on
category pages). Styles are plain list items, not "Product" (Google requires a price for Product).
`public/sitemap.xml` is rebuilt with today's date by every build.

## Redirects and caching

`src/worker.js` sends `www.`, `http://` and the workers.dev preview address to `https://<domain>` with a permanent (301)
redirect, so Google indexes one version of each page, and sets 7-day browser caching for images, CSS and JS.

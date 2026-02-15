# Sita — Natural Tanning & Primitive Skills Website

## Project overview

A multilingual (EN/NL/FR) static website built with a custom Python build script. No framework — just `build.py` reading JSON data + HTML templates from `src/` and outputting fully static pages to `dist/`.

**Single dependency:** `pip install markdown` (inside `.venv`)

## Architecture

```
src/
├── data/           JSON data (site config, translations, products, blog metadata)
├── templates/      HTML templates with {{placeholder}} syntax
├── content/blog/   Markdown blog post bodies (slug.lang.md)
└── assets/         CSS, JS, images, fonts (copied verbatim to dist/)

build.py            Reads src/, renders pages, writes dist/
dist/               Build output — upload this to hosting
```

**Templating:** Simple `{{key}}` replacement via `str.replace`/regex in `build.py`. No Jinja2. Context is a flat dict; translation keys are prefixed `t_` (e.g., `{{t_nav_home}}`).

**Multi-language:** Separate directory per language (`/en/`, `/nl/`, `/fr/`). URL slugs are localized (e.g., `/nl/producten/`). Root `index.html` detects browser language and redirects.

**Slug map** for localized URLs is in `build.py` `SLUG_MAP` dict — update it when adding new page types.

## Key files

- `build.py` — the entire build pipeline (~325 lines)
- `src/data/site.json` — site name, contact email, taglines per language
- `src/data/translations.json` — all UI strings keyed by language
- `src/data/products.json` — product entries with multilingual name/description
- `src/data/blog.json` — blog metadata with multilingual title/summary
- `src/assets/css/main.css` — all styles (earthy palette, responsive)
- `src/assets/js/main.js` — mobile nav toggle + image lightbox

## Common workflows

**Build the site:**
```
source .venv/bin/activate && python3 build.py
```

**Preview locally:**
```
cd dist && python3 -m http.server 8765
```

**Add a product:** Add an entry to `src/data/products.json`, add image to `src/assets/images/products/`, rebuild.

**Add a blog post:** Write `src/content/blog/my-slug.en.md` (+ `.nl.md`, `.fr.md`), add entry to `src/data/blog.json`, add cover image, rebuild.

**Add a UI string:** Add the key to all 3 language objects in `src/data/translations.json`, reference as `{{t_your_key}}` in templates.

## Style conventions

- CSS uses custom properties defined in `:root` in `main.css`
- Palette: cream, tan, bark brown, sage green, ember accent
- Headings use Lora (serif); body uses system sans-serif
- Two breakpoints: mobile < 768px, desktop >= 768px
- Templates use semantic HTML with BEM-ish class names

## Things to watch out for

- Template placeholders inside card partials (product-card, blog-card) need their context to include translation strings — see how `build_blog_listing` merges `t_` keys into the per-card context.
- The `render()` function leaves unmatched `{{placeholders}}` intact (by design, for nested rendering). If you see raw `{{...}}` in output, the context dict is missing a key.
- Blog post Markdown files fall back to English if the requested language file doesn't exist.
- The venv at `.venv/` must be activated before running `build.py`.

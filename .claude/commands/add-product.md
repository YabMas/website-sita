Add a new product to the site. Ask the user for:

1. Product ID (slug, e.g. "elk-hide-bag")
2. Name in English, Dutch, and French
3. Description in English, Dutch, and French
4. Price (e.g. "€ 55")
5. Image filename (or use placeholder.svg)

Then:
- Add the entry to `src/data/products.json`
- If the user provides an image, note where to place it (`src/assets/images/products/`)
- Rebuild the site with `source .venv/bin/activate && python3 build.py`
- Confirm the product appears on the products page for all 3 languages

Add a new blog post to the site. Ask the user for:

1. Post slug (e.g. "bark-tanning-guide")
2. Title in English, Dutch, and French
3. Summary in English, Dutch, and French
4. Date (YYYY-MM-DD)
5. Cover image filename (or use placeholder.svg)
6. Post body — either the user provides content directly, or provides notes for you to draft the Markdown

Then:
- Add the metadata entry to `src/data/blog.json`
- Write the Markdown body files to `src/content/blog/<slug>.en.md`, `<slug>.nl.md`, `<slug>.fr.md`
- If the user provides an image, note where to place it (`src/assets/images/blog/`)
- Rebuild the site with `source .venv/bin/activate && python3 build.py`
- Confirm the post appears on the blog listing and individual post page for all 3 languages

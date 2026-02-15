#!/usr/bin/env python3
"""Build script for the Natural Tanning & Primitive Skills website.

Reads JSON data and HTML templates from src/, renders multilingual static
pages, and outputs them to dist/. Blog post bodies are written in Markdown
and converted to HTML via the `markdown` library.

Usage:
    python3 build.py
"""

import json
import os
import re
import shutil
import sys

try:
    import markdown
except ImportError:
    print("Missing dependency: pip install markdown")
    sys.exit(1)

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")
DATA_DIR = os.path.join(SRC, "data")
TEMPLATE_DIR = os.path.join(SRC, "templates")
CONTENT_DIR = os.path.join(SRC, "content")
ASSETS_DIR = os.path.join(SRC, "assets")

LANGUAGES = ["en", "nl", "fr"]
DEFAULT_LANG = "en"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clean():
    """Remove the dist/ directory."""
    if os.path.exists(DIST):
        shutil.rmtree(DIST)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_data():
    """Load all JSON data files into a single dict."""
    data = {}
    for name in ("site", "translations", "products", "blog"):
        filepath = os.path.join(DATA_DIR, f"{name}.json")
        data[name] = load_json(filepath)
    return data


def load_template(name):
    """Read an HTML template file by its path relative to src/templates/."""
    filepath = os.path.join(TEMPLATE_DIR, name)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def render(template, context):
    """Replace all {{key}} placeholders in *template* with values from *context*.

    Supports dotted keys like {{site.name}} — the dot is just part of the
    flat key string.  Unmatched placeholders are left untouched so that
    nested rendering works.
    """
    def replacer(match):
        key = match.group(1).strip()
        return str(context.get(key, match.group(0)))
    return re.sub(r"\{\{(.+?)\}\}", replacer, template)


def render_markdown(filepath):
    """Convert a Markdown file to an HTML fragment string."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    return markdown.markdown(text, extensions=["extra", "codehilite"])


def write_page(rel_path, html):
    """Write *html* to dist/<rel_path>, creating directories as needed."""
    out = os.path.join(DIST, rel_path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  {rel_path}")


def copy_assets():
    """Copy src/assets/ into dist/assets/."""
    dest = os.path.join(DIST, "assets")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(ASSETS_DIR, dest)


# ---------------------------------------------------------------------------
# URL helpers
# ---------------------------------------------------------------------------

SLUG_MAP = {
    "products": {"en": "products", "nl": "producten", "fr": "produits"},
    "blog":     {"en": "blog",     "nl": "blog",      "fr": "blog"},
}


def page_url(page, lang):
    """Return the relative URL for a given page in the given language."""
    if page == "home":
        return f"/{lang}/"
    slug = SLUG_MAP.get(page, {}).get(lang, page)
    return f"/{lang}/{slug}/"


def blog_post_url(post_slug, lang):
    blog_slug = SLUG_MAP["blog"][lang]
    return f"/{lang}/{blog_slug}/{post_slug}/"


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------

def build_context(lang, data, page="home", extra=None):
    """Build the flat template context dict for a given language and page."""
    site = data["site"]
    t = data["translations"].get(lang, {})

    ctx = {}
    # Site-level
    ctx["lang"] = lang
    ctx["site_name"] = site["name"]
    ctx["site_tagline"] = site["taglines"].get(lang, site["taglines"][DEFAULT_LANG])
    ctx["contact_email"] = site["contact_email"]
    ctx["current_year"] = "2026"

    # Navigation URLs
    ctx["url_home"] = page_url("home", lang)
    ctx["url_products"] = page_url("products", lang)
    ctx["url_blog"] = page_url("blog", lang)

    # Language switcher URLs (point to equivalent page in other languages)
    for l in LANGUAGES:
        if page in ("home", "products", "blog"):
            ctx[f"url_lang_{l}"] = page_url(page, l)
        else:
            # For blog posts, extra should contain the post slug
            slug = (extra or {}).get("post_slug", "")
            if slug:
                ctx[f"url_lang_{l}"] = blog_post_url(slug, l)
            else:
                ctx[f"url_lang_{l}"] = page_url("home", l)

    # Active page marker
    ctx["active_home"] = "active" if page == "home" else ""
    ctx["active_products"] = "active" if page == "products" else ""
    ctx["active_blog"] = "active" if page in ("blog", "blog-post") else ""

    # All translation strings
    for key, val in t.items():
        ctx[f"t_{key}"] = val

    # Page title and description (used in <head>)
    page_key = page if page != "blog-post" else "blog"
    ctx["page_title"] = t.get(f"page_{page_key}_title", site["name"])
    ctx["page_description"] = site["taglines"].get(lang, site["taglines"][DEFAULT_LANG])

    # Merge any extra context
    if extra:
        ctx.update(extra)

    return ctx


def assemble_page(body_html, lang, data, page="home", extra=None):
    """Wrap body_html in the base template with header/footer."""
    ctx = build_context(lang, data, page, extra)

    header = render(load_template("partials/header.html"), ctx)
    footer = render(load_template("partials/footer.html"), ctx)

    ctx["header"] = header
    ctx["footer"] = footer
    ctx["content"] = body_html

    base = load_template("base.html")
    return render(base, ctx)


# ---------------------------------------------------------------------------
# Builders for each page type
# ---------------------------------------------------------------------------

def build_root_redirect():
    """Build the root index.html that detects language and redirects."""
    tpl = load_template("redirect.html")
    write_page("index.html", tpl)


def build_home(lang, data):
    tpl = load_template("home.html")
    ctx = build_context(lang, data, "home")
    body = render(tpl, ctx)
    html = assemble_page(body, lang, data, "home")
    write_page(f"{lang}/index.html", html)


def build_products(lang, data):
    products = data["products"]
    card_tpl = load_template("product-card.html")

    cards_html = ""
    for product in products:
        p_ctx = {
            "product_name": product["name"].get(lang, product["name"][DEFAULT_LANG]),
            "product_description": product["description"].get(lang, product["description"][DEFAULT_LANG]),
            "product_image": product.get("image", "/assets/images/products/placeholder.svg"),
            "product_price": product.get("price", ""),
        }
        cards_html += render(card_tpl, p_ctx)

    tpl = load_template("products.html")
    ctx = build_context(lang, data, "products")
    ctx["product_cards"] = cards_html
    body = render(tpl, ctx)
    html = assemble_page(body, lang, data, "products")

    slug = SLUG_MAP["products"][lang]
    write_page(f"{lang}/{slug}/index.html", html)


def build_blog_listing(lang, data):
    posts = data["blog"]
    card_tpl = load_template("blog-card.html")

    t = data["translations"].get(lang, {})
    cards_html = ""
    for post in posts:
        p_ctx = {f"t_{k}": v for k, v in t.items()}
        p_ctx.update({
            "post_title": post["title"].get(lang, post["title"][DEFAULT_LANG]),
            "post_summary": post["summary"].get(lang, post["summary"][DEFAULT_LANG]),
            "post_date": post["date"],
            "post_image": post.get("image", "/assets/images/blog/placeholder.svg"),
            "post_url": blog_post_url(post["slug"], lang),
        })
        cards_html += render(card_tpl, p_ctx)

    tpl = load_template("blog.html")
    ctx = build_context(lang, data, "blog")
    ctx["blog_cards"] = cards_html
    body = render(tpl, ctx)
    html = assemble_page(body, lang, data, "blog")

    slug = SLUG_MAP["blog"][lang]
    write_page(f"{lang}/{slug}/index.html", html)


def build_blog_posts(lang, data):
    posts = data["blog"]
    tpl = load_template("blog-post.html")
    blog_slug = SLUG_MAP["blog"][lang]

    for post in posts:
        # Locate the markdown file
        md_file = os.path.join(CONTENT_DIR, "blog", f"{post['slug']}.{lang}.md")
        if not os.path.exists(md_file):
            # Fall back to default language
            md_file = os.path.join(CONTENT_DIR, "blog", f"{post['slug']}.{DEFAULT_LANG}.md")
        if not os.path.exists(md_file):
            print(f"  WARNING: No content found for {post['slug']} ({lang}), skipping")
            continue

        body_html = render_markdown(md_file)

        post_title = post["title"].get(lang, post["title"][DEFAULT_LANG])
        extra = {
            "post_slug": post["slug"],
            "post_title": post_title,
            "page_title": post_title,
            "post_date": post["date"],
            "post_image": post.get("image", "/assets/images/blog/placeholder.svg"),
            "post_body": body_html,
            "url_blog_listing": page_url("blog", lang),
        }

        inner = render(tpl, build_context(lang, data, "blog-post", extra))
        html = assemble_page(inner, lang, data, "blog-post", extra)
        write_page(f"{lang}/{blog_slug}/{post['slug']}/index.html", html)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Building site...")
    clean()
    os.makedirs(DIST, exist_ok=True)

    data = load_data()
    copy_assets()
    print("Assets copied.")

    build_root_redirect()

    for lang in LANGUAGES:
        print(f"\n[{lang}]")
        build_home(lang, data)
        build_products(lang, data)
        build_blog_listing(lang, data)
        build_blog_posts(lang, data)

    print("\nDone! Output in dist/")


if __name__ == "__main__":
    main()

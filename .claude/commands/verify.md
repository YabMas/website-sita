Build the site and run a full verification:

1. Run `source .venv/bin/activate && python3 build.py` and confirm it succeeds
2. Check all generated HTML files in `dist/` for unresolved `{{...}}` placeholders
3. Verify the language switcher links are correct (each page links to the correct equivalent in other languages)
4. Verify all referenced assets (CSS, JS, images) exist in `dist/assets/`
5. Count the total pages generated and report the full file listing
6. Report any warnings or issues found

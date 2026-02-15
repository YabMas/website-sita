Add a new UI translation string. The user will provide a key name and the text in English, Dutch, and French.

1. Add the key to all 3 language objects in `src/data/translations.json`
2. Tell the user they can reference it in templates as `{{t_<key>}}`
3. Rebuild the site if the string is already used in a template

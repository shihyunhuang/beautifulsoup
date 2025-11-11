# Milestone-3
## Changed file
### bs4.__init__.py
Apply SoupReplacer transformers on the real Tag object
### bs4.SoupReplacer.py
- Supports both Milestone-2 constructor SoupReplacer(og_tag, alt_tag) and the new transformer-based constructor SoupReplacer(name_xformer=None, attrs_xformer=None, xformer=None).
- Enables tag-name changes, attribute transformations, and arbitrary in-place tag modifications during parsing, avoiding a second traversal of the parse tree.
## New file
### bs4.test.test_replacer_m3.py
Contains six automated tests verifying the new API.
- Tests cover tag renaming, attribute rewriting, attribute removal, nested tag handling, backward compatibility with M2, and combined transformations.
- Run with:
```bash
# Run tests
pytest -v bs4/tests/test_replacer_m3.py
```
### apps.m3.task7.py
Applies all three transformers while parsing sample.html:
- rename <b> → <blockquote>, <em> → <i>
- clean up class="old" and inline styles
- add rel="nofollow noopener" to external links
- ensure <img> has an alt attribute
- Run with:
```bash
# Execute task6 on the sample HTML
python -m apps.m3.task7 apps/m3/sample.html
```


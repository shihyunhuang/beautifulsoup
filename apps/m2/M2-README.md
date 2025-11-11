# Milestone-2
## Milestone-2 Part-1: Modify task by implement SoupStrainer
### Task 2 — Filter tags with href
Parses only the elements that contain an href attribute and prints each tag’s name, href value, and visible text.
```bash
python apps/m2/task2.py apps/m2/sample.html
```
### Task 3 — Extract specific tags or sections
Re‑implements Milestone‑1 Task 3 but uses SoupStrainer to limit parsing to the tags of interest (for example, only <h1>, <h2>, and <a> tags). Output format is the same as in M1.
```bash
python apps/m2/task3.py apps/m2/sample.html
```
### Task 4 — Parse only tables
Processes only <table>, <tr>, <td>, and <th> elements using SoupStrainer. Performs the same computations as in Milestone‑1 Task 4 but more efficiently.
```bash
python apps/m2/task4.py apps/m2/sample.html
```

## Milestone-2 Part-2: BeautifulSoup Source Code Reference

This document lists the **original source files and line numbers** for all BeautifulSoup API functions I used in Milestone-1 and Milestone-2 Part-1.

### Source
- Original zip: `beautifulsoup.zip`
- Extracted path: `Milestone-2/beautifulsoup/`

### API Reference Table
| API | Type | File | Line |
|-----|------|------|------|
| BeautifulSoup | Class | bs4/__init__.py | 133 |
| BeautifulSoup.__init__| Method | bs4/__init__.py | 209 |
| SoupStrainer | Class | bs4/filter.py | 313 |
| SoupStrainer.init | Method | bs4/filter.py | 345 |
| ResultSet | Class | bs4/element.py | 2861 |
| Tag.__iter__ | Method | bs4/element.py | 2208 |
| Tag.prettify() | Method | bs4/element.py | 2601 |
| Tag.get() | Method | bs4/element.py | 2160 |
| Tag.get_text() | Method | bs4/element.py | 524 |
| Tag.__getitem__ | Method | bs4/element.py | 2203 |
| Tag.find_all() | Method | bs4/element.py | 2715 |
| Tag.find_parent() | Method | bs4/element.py | 992 |
| Tag.find_next_sibling() | Method | bs4/element.py | 803 |
| Tag.__setitem__ | Method | bs4/element.py | 2223 |
| Tag.name | Attribute | bs4/element.py | 1342 |
| Tag.attrs | Attribute | bs4/element.py | 1675 |

## Milestone-2 Part-3: BeautifulSoup Source Code Reference
### Objective
Implement `SoupReplacer(og_tag, alt_tag)` to replace HTML tags **during parsing**, similar to `SoupStrainer`.

### Modified Files
- `bs4/SoupReplacer.py` – defines `SoupReplacer` class  
- `bs4/__init__.py` – adds `replacer` parameter to `BeautifulSoup`  
- `bs4/builder/_htmlparser.py` – applies tag mapping inside `handle_starttag` / `handle_endtag`  
- `bs4/tests/test_replacer.py` – test cases for tag replacement  
- `apps/m2/task6.py` – reads HTML file and applies `SoupReplacer`

### Run
```bash
# Execute task6 on the sample HTML
python -m apps.m2.task6 apps/m2/sample.html

# Run tests
python -m unittest bs4.tests.test_replacer
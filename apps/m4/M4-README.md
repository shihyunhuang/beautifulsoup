# Milestone-4
## Changed file
### bs4.__init__.py
A new __iter__() method was added
- The iterator performs a depth–first, pre–order traversal of the parse tree.
- The implementation is a lazy generator that yields nodes one-by-one without collecting them into a list, fully satisfying the assignment requirement.

### bs4.test.test_replacer_m3.py
Contains five automated tests verifying the new iterate API.
- Test 1: Empty document
- Test 2: Document containing only a text node
- test 3: Nested tags
- Test 4: Multiple sibling elements
- Test 5: Mixed node types
- Run with:
```bash
# Run tests
pytest -v bs4/tests/test_iterate.py
```
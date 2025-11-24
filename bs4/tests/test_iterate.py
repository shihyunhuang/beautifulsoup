import pytest
from bs4 import BeautifulSoup, Tag, NavigableString, Comment

def _names_or_text(nodes):
    """Helper: turn nodes into comparable sequence (tag name or text)."""
    out = []
    for n in nodes:
        if isinstance(n, Tag):
            out.append(n.name)
        else:
            out.append(str(n))
    return out


def test_iter_empty_document():
    soup = BeautifulSoup("", "html.parser")
    nodes = list(soup)
    assert nodes == []


def test_iter_only_text_node():
    soup = BeautifulSoup("hello", "html.parser")
    nodes = list(soup)

    # Should yield exactly one NavigableString
    assert len(nodes) == 1
    assert isinstance(nodes[0], NavigableString)
    assert str(nodes[0]) == "hello"


def test_iter_nested_tags_preorder():
    soup = BeautifulSoup("<div>hi<b>yo</b></div>", "html.parser")
    nodes = list(soup)

    # Pre-order DFS: div -> "hi" -> b -> "yo"
    assert _names_or_text(nodes) == ["div", "hi", "b", "yo"]

    # Check types at key spots
    assert isinstance(nodes[0], Tag)                # <div>
    assert isinstance(nodes[1], NavigableString)    # "hi"
    assert isinstance(nodes[2], Tag)                # <b>
    assert isinstance(nodes[3], NavigableString)    # "yo"


def test_iter_multiple_siblings_order():
    soup = BeautifulSoup("<p>1</p><p>2</p>", "html.parser")
    nodes = list(soup)

    # Document order: first p -> "1" -> second p -> "2"
    assert _names_or_text(nodes) == ["p", "1", "p", "2"]


def test_iter_mixed_types_comment_and_self_closing():
    html = "<a href='x'>link<!--c--><img src='y'/></a>"
    soup = BeautifulSoup(html, "html.parser")
    nodes = list(soup)

    # Expected order: a -> "link" -> comment -> img
    assert _names_or_text(nodes) == ["a", "link", "c", "img"]

    # Verify node types and attributes
    assert isinstance(nodes[0], Tag) and nodes[0].name == "a"
    assert nodes[0]["href"] == "x"

    assert isinstance(nodes[1], NavigableString) and str(nodes[1]) == "link"

    assert isinstance(nodes[2], Comment) and str(nodes[2]) == "c"

    assert isinstance(nodes[3], Tag) and nodes[3].name == "img"
    assert nodes[3]["src"] == "y"

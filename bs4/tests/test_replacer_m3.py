import pytest
from bs4 import BeautifulSoup
from bs4.SoupReplacer import SoupReplacer

def test_name_xformer_simple():
    html = "<b>Hello</b>"
    repl = SoupReplacer(name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name)
    soup = BeautifulSoup(html, "html.parser", replacer=repl)
    assert soup.find("blockquote").string == "Hello"
    assert soup.find("b") is None

def test_attrs_xformer_replace_class():
    html = '<p class="old" id="x">Hi</p>'
    repl = SoupReplacer(attrs_xformer=lambda tag: {"class": ["new"], "id": "x"})
    soup = BeautifulSoup(html, "html.parser", replacer=repl)
    p = soup.find("p")
    assert p["class"] == ["new"]
    assert p["id"] == "x"

def test_xformer_remove_class():
    html = '<div class="c1 c2">X</div>'
    def rm(tag):
        if "class" in tag.attrs:
            del tag.attrs["class"]
    soup = BeautifulSoup(html, "html.parser", replacer=SoupReplacer(xformer=rm))
    assert soup.div.has_attr("class") is False

def test_nested_rename():
    html = "<b><b>inner</b></b>"
    repl = SoupReplacer(name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name)
    soup = BeautifulSoup(html, "html.parser", replacer=repl)
    assert len(soup.find_all("blockquote")) == 2

def test_legacy_ctor_works():
    soup = BeautifulSoup("<b>X</b>", "html.parser", replacer=SoupReplacer("b", "blockquote"))
    assert soup.find("blockquote").string == "X"

def test_name_and_attrs_both():
    html = '<em class="a">t</em>'
    def to_i(tag): return "i" if tag.name == "em" else tag.name
    def mark(tag): return {"class": ["a", "m3"]}
    soup = BeautifulSoup(html, "html.parser",
                         replacer=SoupReplacer(name_xformer=to_i, attrs_xformer=mark))
    el = soup.find("i")
    assert el["class"] == ["a", "m3"]

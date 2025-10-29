# bs4/tests/test_replacer.py
import unittest, re
from bs4 import BeautifulSoup, SoupReplacer

# 幫手：確認某個標籤（含開/閉）不存在字串中
def _no_tag(name: str, s: str) -> bool:
    # <b ...> 或 </b>，右邊界是空白或 >
    pattern = re.compile(rf"<\s*/?\s*{re.escape(name)}(?=\s|>)", re.IGNORECASE)
    return pattern.search(s) is None

class TestSoupReplacer(unittest.TestCase):
    def test_replace_all_and_preserve_attributes(self):
        html = """
        <div id="root">
          <p>Normal <b class="bold" data-x="1">text</b> and <i>italic</i>.</p>
          <section>
            <b style="color:red">inside section</b>
            <span><b>nested <b>deep</b></b></span>
          </section>
          <br/>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser",
                             replacer=SoupReplacer("b", "blockquote"))

        # No more tag <b> 
        self.assertEqual(len(soup.find_all("b")), 0)

        # There should be 4 <blockquote>
        self.assertEqual(len(soup.find_all("blockquote")), 4)

        # Attributes aren't changed
        blk = soup.find("blockquote", {"class": "bold"})
        self.assertIsNotNone(blk)
        self.assertEqual(blk.get("data-x"), "1")

        # Other tags aren't changed
        self.assertEqual(len(soup.find_all("i")), 1)
        self.assertEqual(len(soup.find_all("br")), 1)

        # 渲染文字中不應有真正的 <b> 或 </b> 標籤
        text = soup.prettify()
        self.assertTrue(_no_tag("b", text))

    def test_noop_when_no_match(self):
        html = """
        <article>
          <h1>Title</h1>
          <p><i>only italic</i> and <u>underline</u>.</p>
        </article>
        """
        soup = BeautifulSoup(html, "html.parser",
                             replacer=SoupReplacer("b", "blockquote"))
        self.assertEqual(len(soup.find_all("blockquote")), 0)
        self.assertEqual(len(soup.find_all("h1")), 1)
        self.assertEqual(len(soup.find_all("i")), 1)
        self.assertEqual(len(soup.find_all("u")), 1)

if __name__ == "__main__":
    unittest.main()

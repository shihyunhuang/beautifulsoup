class SoupReplacer:
    """
    During-parsing tag replacer.
    Example:
        replacer = SoupReplacer("b", "blockquote")
        soup = BeautifulSoup(html_doc, "html.parser", replacer=replacer)
        print(soup.prettify())
    """
    def __init__(self, og_tag: str, alt_tag: str):
        # Store the tag names to be replaced, and convert them to lowercase to avoid case differences.
        self.og_tag = (og_tag or "").lower()
        self.alt_tag = (alt_tag or "").lower()

    def map(self, name: str) -> str:
        """If the tag name matches og_tag, return alt_tag; otherwise, return it as is."""
        if name and name.lower() == self.og_tag:
            return self.alt_tag
        return name
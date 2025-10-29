from pathlib import Path
from bs4 import BeautifulSoup, SoupStrainer
import sys

# Print all rows in xml
def task2(file_name):
    path = Path(file_name)
    suffix = path.suffix.lower()
    if suffix == '.xml':
        raise ValueError("XML is not supported for this task. Please provide an HTML file.")
    
    # Define the strainer
    def has_href(name, attrs):
        return bool(attrs) and any(k.lower() == "href" for k in attrs.keys())
    
    only_links = SoupStrainer(has_href)
    with open(path, "rb") as f:
        soup = BeautifulSoup(f, "html.parser", parse_only=only_links)

    for tag in soup:
        href_key = next((k for k in tag.attrs if k.lower() == "href"), None)
        if href_key:
            href = tag.attrs.get(href_key, "")
            text = (tag.get_text(strip=True) or "").strip()
            print(f"Tag: {tag.name}, href={href}, text={text}")
            found = True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task2.py <html_file>")
    else:
        task2(sys.argv[1])
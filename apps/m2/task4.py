from pathlib import Path
from bs4 import BeautifulSoup, SoupStrainer
import sys

# Print all tags contain ID
def task4(file_name):
    path = Path(file_name)
    suffix = path.suffix.lower()
    parser = 'xml' if suffix == '.xml' else 'html.parser'
    # Function that helps Strainer to get "Id" attrs
    def want(name, attrs):
        if attrs:
            return any(k.lower() == "id" for k in attrs.keys())
        return False
    only_with_id = SoupStrainer(want)
    
    with open(path, "rb") as f:
        soup = BeautifulSoup(f, parser, parse_only=only_with_id)

    for tag in soup:
        id_key = next((k for k in tag.attrs.keys() if k.lower() == "id"), None)
        if id_key:
            print(f"Tag: {tag.name}, ID: {tag.attrs[id_key]}")
            found = True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task4.py <file>")
    else:
        task4(sys.argv[1])
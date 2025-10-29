from pathlib import Path
from bs4 import BeautifulSoup, SoupStrainer
import sys

# Print all tags in xml
def task3(file_name):
    path = Path(file_name)
    only_tags = SoupStrainer(True)  # Get all tags
    suffix = path.suffix.lower()
    parser = 'xml' if suffix == '.xml' else 'html.parser'

    with open(path, "rb") as f:
        soup = BeautifulSoup(f, parser, parse_only=only_tags)

    # Due to get all, it should use find all or it will only print the tag on the top
    for tag in soup.find_all(True):
        print(tag.name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task3.py <file>")
    else:
        task3(sys.argv[1])
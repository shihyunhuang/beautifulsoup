from pathlib import Path
from bs4 import BeautifulSoup, SoupReplacer
import time
import sys

def task6(file_name: str):
    """Milestone-2 Task-6 using SoupReplacer (during parsing)"""
    start_time = time.time()
    path = Path(file_name)
    if path.suffix.lower() != ".html":
        raise ValueError("Unsupported file type. Please provide an HTML file.")

    # Read html
    html_text = path.read_text(encoding="utf-8")

    # Replace <b> → <blockquote>
    replacer = SoupReplacer("b", "blockquote")
    soup = BeautifulSoup(html_text, "html.parser", replacer=replacer)

    # Output a new html file
    output_file = path.parent / f"task6_{path.name}"
    output_file.write_text(soup.prettify(), encoding="utf-8")

    print(f"✅ Converted '{file_name}' → '{output_file.name}'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task6.py <html_file>")
    else:
        task6(sys.argv[1])

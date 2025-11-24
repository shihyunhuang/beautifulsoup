from pathlib import Path
from bs4 import BeautifulSoup, SoupReplacer
import time
import sys

def task7(file_name: str):
    """Milestone-3 Task-7 using SoupReplacer (during parsing with transformers)"""
    start_time = time.time()
    path = Path(file_name)
    if path.suffix.lower() != ".html":
        raise ValueError("Unsupported file type. Please provide an HTML file.")

    # Read html
    html_text = path.read_text(encoding="utf-8")

    # ---------------- Define the transformers ----------------
    def name_xformer(tag):
        if tag.name == "b":
            return "blockquote"
        if tag.name == "em":
            return "i"
        return tag.name

    def attrs_xformer(tag):
        attrs = dict(tag.attrs or {})
        if tag.name == "a":
            href = attrs.get("href", "")
            if href.startswith("http://") or href.startswith("https://"):
                existing_rel = set()
                rel_val = attrs.get("rel", [])
                if isinstance(rel_val, str):
                    existing_rel.update(rel_val.split())
                elif isinstance(rel_val, (list, tuple)):
                    existing_rel.update(rel_val)
                existing_rel.update(["noopener", "nofollow"])
                attrs["rel"] = sorted(existing_rel)
        return attrs

    def xformer(tag):
        # Remove inline styles
        if "style" in tag.attrs:
            del tag.attrs["style"]

        # Remove class="old"
        if "class" in tag.attrs:
            classes = tag.attrs.get("class", [])
            if isinstance(classes, str):
                classes = classes.split()
            classes = [c for c in classes if c != "old"]
            if classes:
                tag.attrs["class"] = classes
            else:
                del tag.attrs["class"]

        # Add missing alt to <img>
        if tag.name == "img" and "alt" not in tag.attrs:
            tag.attrs["alt"] = ""

    # Create replacer
    replacer = SoupReplacer(
        name_xformer=name_xformer,
        attrs_xformer=attrs_xformer,
        xformer=xformer,
    )

    # Parse & transform
    soup = BeautifulSoup(html_text, "html.parser", replacer=replacer)

    # Output a new html file
    output_file = path.parent / f"task7_{path.name}"
    output_file.write_text(soup.prettify(), encoding="utf-8")

    elapsed = time.time() - start_time
    print(f"Converted '{file_name}' → '{output_file.name}' ({elapsed:.2f}s)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m apps.m3.task7 <html_file>")
    else:
        task7(sys.argv[1])

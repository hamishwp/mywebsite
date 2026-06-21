#!/usr/bin/env python3
"""Generate sitemap.xml from the HTML pages in the project root.
Run after adding/removing pages:  python3 build_sitemap.py
(The literature/claywork generators add pages, so run this last.)
"""
import pathlib, datetime

ROOT = pathlib.Path(__file__).parent
BASE = "https://hamishwp.github.io/mywebsite/"
EXCLUDE = set()  # add filenames here to keep them out of the sitemap

# Rough priority hints (default 0.6). Home highest.
PRIORITY = {
    "index.html": "1.0", "cv.html": "0.9", "science.html": "0.9",
    "visual-art.html": "0.8", "claywork.html": "0.7",
    "short-stories.html": "0.7", "poetry.html": "0.7", "contact.html": "0.6",
}

def url_for(name):
    return BASE if name == "index.html" else BASE + name

def main():
    today = datetime.date.today().isoformat()
    pages = sorted(p.name for p in ROOT.glob("*.html") if p.name not in EXCLUDE)
    # Put core pages first, then the rest.
    core = [p for p in PRIORITY if p in pages]
    rest = [p for p in pages if p not in PRIORITY]
    ordered = core + rest

    rows = []
    for name in ordered:
        rows.append(
            "  <url>\n"
            f"    <loc>{url_for(name)}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <priority>{PRIORITY.get(name, '0.6')}</priority>\n"
            "  </url>"
        )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"Wrote sitemap.xml with {len(ordered)} URLs (lastmod {today}).")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render the Science and Visual Art pages from the spreadsheets, as STATIC HTML
(so search engines and AI crawlers see the content without running JavaScript).

For each page it injects, between markers:
  - the work cards  (<!-- CARDS:START --> ... <!-- CARDS:END -->) in the body
  - JSON-LD structured data (<!-- JSONLD:START --> ... <!-- JSONLD:END -->) in <head>

Run after editing a spreadsheet:
    python3 build_data.py            # both
    python3 build_data.py science    # just science
    python3 build_data.py visual_art # just visual art

Content is taken VERBATIM from the spreadsheet; only image paths are mapped to the
file that actually exists on disk (e.g. 'bp.png' -> 'bp.jpg') so images never 404.
"""
import json, re, sys, html, pathlib
import openpyxl

ROOT = pathlib.Path(__file__).parent
BASE = "https://hamishwp.github.io/mywebsite/"
AUTHOR = {"@type": "Person", "name": "Hamish Patten"}

PAGES = {
    "science":    dict(sheet="science.xlsx",    page="science.html",
                       container="science-cards", show_link=True,  itemtype="ScholarlyArticle"),
    "visual_art": dict(sheet="visual_art.xlsx", page="visual-art.html",
                       container="art-cards",     show_link=False, itemtype="VisualArtwork"),
}

def resolve_image(rel):
    if not rel:
        return rel
    if (ROOT / rel).exists():
        return rel
    stem = (ROOT / rel).with_suffix("")
    for ext in (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"):
        cand = stem.with_suffix(ext)
        if cand.exists():
            return str(cand.relative_to(ROOT))
    print(f"  ! warning: no image file found for '{rel}'")
    return rel

def read_sheet(path):
    ws = openpyxl.load_workbook(path).active
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(h).strip() for h in rows[0]]
    items = []
    for r in rows[1:]:
        if not any(r):
            continue
        row = {hdr[i]: (r[i] if i < len(r) else None) for i in range(len(hdr))}
        url = (row.get("File") or "").strip()
        items.append({
            "title":    (row.get("Title") or "").strip(),
            "subtitle": (row.get("Subtitle") or "").strip(),
            "image":    resolve_image((row.get("Image") or "").strip()),
            "text":     (row.get("Text") or "").strip(),
            "url":      url,
        })
    return items

def first_words(text, n=30):
    words = text.split()
    if len(words) <= n:
        return text, False
    return " ".join(words[:n]) + "…", True

def render_card(it, show_link):
    e = html.escape
    teaser, trunc = first_words(it["text"])
    url = it["url"]
    link = ""
    if show_link and url and not url.endswith("="):   # skip incomplete/placeholder URLs
        link = f' <a href="{e(url)}" target="_blank" rel="noopener">(see the full article here)</a>'
    if trunc:
        body = (f'<p class="card-teaser">{e(teaser)}</p>'
                f'<p class="card-full" hidden>{e(it["text"])}</p>'
                f'<button class="expand-btn" type="button">Read more</button>')
    else:
        body = f'<p>{e(it["text"])}</p>'
    return ('      <article class="card">\n'
            f'        <div class="card-frame"><img src="{e(it["image"])}" alt="{e(it["title"])}" loading="lazy"></div>\n'
            f'        <h3 class="card-title">{e(it["title"])}</h3>\n'
            f'        <p class="card-subtitle"><em>{e(it["subtitle"])}</em>{link}</p>\n'
            f'        <div class="card-body">{body}</div>\n'
            '      </article>')

def json_ld(items, cfg):
    elements = []
    for i, it in enumerate(items, 1):
        work = {
            "@type": cfg["itemtype"],
            "name": it["title"],
            "image": BASE + it["image"],
            "description": it["text"],
        }
        if cfg["itemtype"] == "ScholarlyArticle":
            work["headline"] = it["title"]
            work["author"] = AUTHOR
            if it["url"] and not it["url"].endswith("="):
                work["url"] = it["url"]
        else:
            work["creator"] = AUTHOR
            work["artform"] = "Painting"
            if it["subtitle"]:
                work["locationCreated"] = it["subtitle"]
        elements.append({"@type": "ListItem", "position": i, "item": work})
    data = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": elements}
    return ('  <script type="application/ld+json">\n  '
            + json.dumps(data, ensure_ascii=False, indent=2).replace("\n", "\n  ")
            + "\n  </script>")

def splice(text, start, end, replacement):
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pat.search(text):
        raise SystemExit(f"Markers not found: {start} ... {end}")
    return pat.sub(lambda m: f"{start}\n{replacement}\n    {end}", text, count=1)

def build(key):
    cfg = PAGES[key]
    items = read_sheet(ROOT / "spreadsheets" / cfg["sheet"])
    page = ROOT / cfg["page"]
    text = page.read_text(encoding="utf-8")
    cards = "\n".join(render_card(it, cfg["show_link"]) for it in items)
    text = splice(text, "<!-- CARDS:START -->", "<!-- CARDS:END -->", cards)
    text = splice(text, "<!-- JSONLD:START -->", "<!-- JSONLD:END -->", json_ld(items, cfg))
    page.write_text(text, encoding="utf-8")
    print(f"Updated {cfg['page']} ({len(items)} entries) from {cfg['sheet']}")

def main():
    which = sys.argv[1:] or list(PAGES)
    for key in which:
        if key not in PAGES:
            raise SystemExit(f"Unknown section '{key}'. Use: {', '.join(PAGES)}")
        build(key)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate the Literature pages (indexes + one page per story/poem) from
site_structure_ideas/literature.md. Re-run after editing that file:
    python3 build_literature.py
"""
import re, html, json, pathlib

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "site_structure_ideas" / "literature.md"
BASE = "https://hamishwp.github.io/mywebsite/"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital@0;1&family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">')

def meta_block(title, filename, description, og_type, jsonld):
    e = html.escape
    canon = BASE + filename
    t = e(title) + " — Hamish Patten"
    d = e(description)
    tags = [
        f'<meta name="description" content="{d}">',
        '<meta name="author" content="Hamish Patten">',
        f'<link rel="canonical" href="{canon}">',
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
        '<meta name="theme-color" content="#1B3A2B">',
        f'<meta property="og:type" content="{og_type}">',
        '<meta property="og:site_name" content="Hamish Patten">',
        f'<meta property="og:title" content="{t}">',
        f'<meta property="og:description" content="{d}">',
        f'<meta property="og:url" content="{canon}">',
        '<meta name="twitter:card" content="summary">',
        f'<meta name="twitter:title" content="{t}">',
        f'<meta name="twitter:description" content="{d}">',
    ]
    block = "\n  ".join(tags)
    if jsonld:
        block += "\n  " + jsonld
    return block

def jsonld_creativework(title, filename, genre, collection_name, collection_file):
    data = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": title,
        "headline": title,
        "genre": genre,
        "inLanguage": "en",
        "author": {"@type": "Person", "name": "Hamish Patten"},
        "url": BASE + filename,
        "isPartOf": {"@type": "CollectionPage", "name": collection_name, "url": BASE + collection_file},
    }
    return ('<script type="application/ld+json">\n  '
            + json.dumps(data, ensure_ascii=False, indent=2).replace("\n", "\n  ")
            + "\n  </script>")

def excerpt(text, n=155):
    flat = " ".join(text.split())
    return (flat[:n].rsplit(" ", 1)[0] + "…") if len(flat) > n else flat

def page(title, body, data_page, filename, description, og_type="website", jsonld=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} — Hamish Patten</title>
  {meta_block(title, filename, description, og_type, jsonld)}
  {FONTS}
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body data-page="{data_page}">
  <div id="site-header"></div>

  <main class="page container">
{body}
  </main>

  <div id="site-footer"></div>
  <script src="assets/site.js"></script>
</body>
</html>
"""

def slugify(s):
    s = s.lower().replace("'", "").replace("’", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def parse(md):
    section = None
    title = None
    buf = []
    items = []  # (section, title, text)
    def flush():
        if title is not None:
            items.append((section, title, "\n".join(buf).strip()))
    for line in md.splitlines():
        if re.match(r"^#\s", line):
            flush(); title = None; buf = []
            low = line.lower()
            section = "stories" if "short stories" in low else ("poetry" if "poetry" in low else section)
        elif line.startswith("## "):
            flush(); title = line[3:].strip(); buf = []
        else:
            if title is not None:
                buf.append(line)
    flush()
    return items

def blocks(text):
    """Split into paragraphs/stanzas on blank lines."""
    return [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]

def story_page(title, text):
    fn = f"story-{slugify(title)}.html"
    paras = "\n".join(f"    <p>{html.escape(b)}</p>" for b in blocks(text))
    body = (f'    <a class="back-link" href="short-stories.html">← Short Stories</a>\n'
            f'    <article class="prose">\n'
            f'    <h1>{html.escape(title)}</h1>\n'
            f'{paras}\n'
            f'    </article>')
    jl = jsonld_creativework(title, fn, "Short story", "Short Stories", "short-stories.html")
    return page(title, body, "short-stories", fn, excerpt(text), "article", jl)

def poem_page(title, text):
    fn = f"poem-{slugify(title)}.html"
    # preserve line breaks within stanzas (CSS .poem uses white-space: pre-line)
    stanzas = "\n".join(f"    <p>{html.escape(b)}</p>" for b in blocks(text))
    body = (f'    <a class="back-link" href="poetry.html">← Poetry</a>\n'
            f'    <article class="prose poem">\n'
            f'    <h1>{html.escape(title)}</h1>\n'
            f'{stanzas}\n'
            f'    </article>')
    jl = jsonld_creativework(title, fn, "Poem", "Poetry", "poetry.html")
    return page(title, body, "poetry", fn, excerpt(text), "article", jl)

def index_page(kind, entries, lede):
    label = "Short Stories" if kind == "stories" else "Poetry"
    fn = "short-stories.html" if kind == "stories" else "poetry.html"
    links = "\n".join(
        f'      <a class="lit-link" href="{ef}"><span class="t">{html.escape(t)}</span></a>'
        for (t, ef) in entries)
    body = (f'    <h1>{label}</h1>\n'
            f'    <p class="lede">{lede}</p>\n'
            f'    <hr class="rule">\n'
            f'    <div class="lit-index">\n{links}\n    </div>')
    data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": label + " — Hamish Patten",
        "url": BASE + fn,
        "hasPart": [{"@type": "CreativeWork", "name": t, "url": BASE + ef} for (t, ef) in entries],
    }
    jl = ('<script type="application/ld+json">\n  '
          + json.dumps(data, ensure_ascii=False, indent=2).replace("\n", "\n  ") + "\n  </script>")
    return page(label, body, kind, fn, lede, "website", jl)

def main():
    md = SRC.read_text(encoding="utf-8")
    items = parse(md)
    story_entries, poem_entries = [], []
    written = []
    for section, title, text in items:
        if section == "stories":
            fn = f"story-{slugify(title)}.html"
            (ROOT / fn).write_text(story_page(title, text), encoding="utf-8")
            story_entries.append((title, fn)); written.append(fn)
        elif section == "poetry":
            fn = f"poem-{slugify(title)}.html"
            (ROOT / fn).write_text(poem_page(title, text), encoding="utf-8")
            poem_entries.append((title, fn)); written.append(fn)

    (ROOT / "short-stories.html").write_text(index_page(
        "stories", story_entries,
        "A handful of short stories written over the years. Click a title to read."),
        encoding="utf-8")
    (ROOT / "poetry.html").write_text(index_page(
        "poetry", poem_entries,
        "A small collection of poems. Click a title to read."),
        encoding="utf-8")
    written += ["short-stories.html", "poetry.html"]

    print(f"Generated {len(written)} pages:")
    for w in written:
        print("  ", w)

if __name__ == "__main__":
    main()

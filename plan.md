# Website Build Plan — Hamish Patten

A summary of what I understand from the `site_structure_ideas/` files and what I'll
need to build the site. Read the **Open Questions** section at the bottom — I need
answers there before I can build cleanly.

---

## 1. Goal & constraints

- A **personal "online CV"** site spanning **science + art**, hosted on **GitHub Pages**.
- **Static HTML/CSS/JS** — no server, no database. GitHub Pages serves files directly.
- **Fully responsive**: must work on phone and laptop. Layouts reflow by screen width.
- Classy, gallery-like, "scientist-who-paints" feel. Restrained, elegant, content-forward.

## 2. Recommended tech approach

- **Plain HTML + CSS + a little vanilla JS.** No framework needed; keeps it fast,
  portable, and zero-maintenance on GitHub Pages.
- **CSS custom properties (design tokens)** for colours, fonts and spacing so the
  whole palette/typography can be changed in one place while we tune it.
- **One shared stylesheet** (`styles.css`) + **one shared header/footer** injected
  by a tiny JS include (or duplicated per page — see Q7).
- **Mobile-first CSS** with breakpoints (~600px phone → tablet → ~1000px laptop).
- **Data**: the two spreadsheets are converted **once** into the page content. I'll
  most likely hard-code them into the HTML (or a small `data.js`) rather than parse
  `.xlsx` in the browser, since GitHub Pages can't run the conversion. See Q6.

## 3. Site map

| Page | Source file | Notes |
|------|-------------|-------|
| **Home** | `home.md` | Intro text + one teaser card per page |
| **CV** | `cv.md` | Display the CV — **approach undecided, see Q1** |
| **Science** | `science.md` + `science.xlsx` | 7 publications, expandable cards |
| **Visual Art** | `visual_art.md` + `visual_art.xlsx` | 6 paintings, expandable cards |
| **Claywork** | `pottery.md` | **Deferred** — empty, waiting on photos |
| **Literature** | `literature.md` | Dropdown → Short Stories / Poetry |
| **Contact** | `contact.md` | **Empty — needs content, see Q4** |

**Header** (per `general_website.md`): "Hamish Patten" far left, then nav:
**CV · Science · Visual Art · Claywork · Literature ▾ · Contact**.
Literature is a **dropdown** with two children: *Short Stories* and *Poetry*.
On mobile the nav collapses to a hamburger menu.

## 4. Page-by-page detail

### Home
- Intro text is currently **empty** (`""`) — I need it, or I'll draft one for approval (Q4).
- One section per page (CV, Science, Visual Art, Claywork, Literature, Contact), each
  with an image + a short teaser line linking through. I'll pull representative images
  (e.g. self-portrait for Visual Art, a paper figure for Science) and draft teaser copy.

### Science
- Intro text supplied (mentions Google Scholar link — I'll hyperlink it).
- 7 rows from `science.xlsx` → one card each. Columns: Title, Subtitle, Text, File (URL), Image.
- Card: **image centred on top**, then **title (large/bold)**, **subtitle (large/italic)**,
  then body text.
- The subtitle gets an appended hyperlink **"(see the full article here)"** → the `File` URL.
- **Collapsed by default**: show title + subtitle + first ~30 words, with an **expand**
  control to reveal the full `Text`.
- Responsive grid: **1 card per row on phone, 2 cards per row on laptop** (see Q5 about the "two-column text").

### Visual Art
- Intro text supplied. 6 rows from `visual_art.xlsx`, same card pattern as Science but
  **no article URL** (the `File` column is empty for paintings).
- Same expand-to-read and 1-up mobile / 2-up laptop behaviour.
- **Background matters most here** — see colour section.

### Literature
- Split into **Short Stories** (4) and **Poetry** (8), reachable via the header dropdown.
  - Short stories: *All Rivers End at the Sea*, *Corridors*, *Taobrick Home*, *The Light Went Out*
  - Poetry: *Etherial Shrinkage*, *Change*, *Our Rading Reflections*, *The Great Lake*,
    *Tunnel Vision*, *Two Dancing Flies*, *Treat Me Like I'm Worthless*
- `literature.md` says **one page per story**. I propose: a **Short Stories index**
  (list of titles → individual story pages) and a **Poetry** page (poems are shorter,
  can sit on one scrollable page, or also one-per-page). See Q3.

### CV
- Show the CV with the **self-portrait painting** as the photo, reusing the same
  frame/border treatment as on the Visual Art page. **Build approach is the key open
  decision — see Q1.**

### Contact
- Currently empty. Needs: what to show (email, social/professional links, a form?). See Q4.

## 5. Colour scheme (my recommendation)

You mentioned **dark Victorian green** header fill, **gold** header text / section
dividers, and a **complementary purple** for a small minority of the site. That's a
strong, classy direction and it works well for an art+science site. Concrete proposal:

| Role | Suggested hex | Notes |
|------|---------------|-------|
| Header fill / dark green | `#1B3A2B` (deep hunter) or `#14342B` | Brunswick/British-racing feel |
| Gold (header text, dividers, links) | `#C9A24B` (antique gold) | Softer than bright `#D4AF37`; reads well on green |
| Purple accent (sparing) | `#4B2E4A` (aubergine) or `#5D3A66` | Pull-quotes, hovers, the odd heading |
| **Art-page background** | `#FFFFFF` pure white | **Yes — keep paintings on true white** |
| General page background | `#FAF8F4` warm off-white / parchment | Gentler than pure white for text pages |
| Body text | `#1E1E1E` near-black | High contrast, easy reading |

**On the white-background question:** yes — for the **Visual Art** (and CV photo)
areas use **pure white** so nothing tints the paintings. For text-heavy pages a warm
off-white (`#FAF8F4`) is easier on the eye and feels "gallery catalogue". The dark
green header + gold framing ties it all together regardless of body background.
The purple is best reserved for tiny moments (a hover state, a pull-quote, the
Literature section accent) so it stays special. See `inspiration.md` for full palettes.

## 6. Typography (font-sampling plan)

You want to choose the font by eye. **The first Home build will include a font-sampler
block** that renders the same heading + paragraph in **10–15 candidate fonts**, stacked
and labelled, so you can browse and confirm once the site is live. All are free Google
Fonts. Shortlist (elegant serif/display, Victorian-leaning):

1. Playfair Display  2. Cormorant Garamond  3. EB Garamond  4. Lora  5. Cardo
6. Crimson Pro  7. Libre Baskerville  8. Spectral  9. Source Serif 4  10. Marcellus
11. Cinzel (Roman caps — very Victorian)  12. Bodoni Moda  13. Prata  14. Italiana
15. Frank Ruhl Libre

**My default for the rest of the site (until you pick):**
- **Headings / wordmark:** **Playfair Display** (elegant, high-contrast, classic).
- **Body text:** **EB Garamond** (warm, very readable — good for the literature pages).

**Easy to swap:** fonts are wired to **two CSS variables** in `styles.css`:
```css
:root {
  --font-display: "Playfair Display", serif;  /* headings  */
  --font-body:    "EB Garamond", serif;        /* body text */
}
```
Changing the site's typography = editing these two lines (the sampler shows you exactly
what to put there). Once you confirm, I remove the sampler block. See Q2.

## 7. Components to build

- Responsive sticky header with dropdown + mobile hamburger.
- Reusable **expandable card** (image + title + subtitle + clamped text + expand toggle).
- Responsive card grid (1-up mobile / 2-up laptop).
- Framed-image treatment (used for paintings and the CV self-portrait).
- Footer (contact / social links).
- Font sampler block (home page, first build only).

## 8. Known issues / cleanups I'll handle

- **Image filename mismatches** between spreadsheets and disk:
  - `science.xlsx` says `bp.png` → actual file is `bp.jpg`.
  - `visual_art.xlsx` says `folklor.jpg`/`brighton.jpg`/`goldhill.jpg` → actual files are `.jpeg`.
  - `Images/Science/idmc_oddrin.png` exists but isn't referenced (unused?).
  I'll normalise these so images resolve correctly. (Flagging in case any are wrong files.)
- `contact.md`, `pottery.md` and the home intro are empty.

---

## 9. Decisions made (2026-06-21)

- **CV page:** **Embed the existing PDF** in a viewer frame + download link. → I need
  the **CV PDF added to the repo** (see Q4).
- **Build-out style:** **Style A — Gallery catalogue** (calm off-white, white art walls,
  dark-green header, gold hairline dividers, shared elegant card; framed self-portrait on CV).
- **Colour palette:** **Palette 1 — Hunter green & antique gold** (`#1B3A2B` / `#C9A24B`
  / aubergine `#4B2E4A` / off-white `#FAF8F4` / white art walls).
- **Poetry:** **one page per poem** (same pattern as the short stories).

## 10. Open Questions

**Q2 — Fonts.** Happy with the 15-font sampler approach? Any fonts you already love
or want added/removed?

**Q4 — Missing copy & files.** Please add the **CV PDF** to the repo, and give me (or
shall I draft for your approval): the **Home intro text**, the **Contact page** content
(email? LinkedIn/Google Scholar/Instagram?), and **Home teaser lines** for each section?

**Q5 — "Two-column text" on Science/Visual Art.** The notes say image centred with text
"split into two columns underneath", *and* "two images side-by-side on laptop". Those
slightly conflict. My plan: **2 cards per row on laptop, 1 on mobile**, each card a single
text column. Do you instead want each card's body text in **two columns** on wide screens?

**Q6 — Data source of truth.** Once I bake the spreadsheet content into the site, future
edits mean editing the HTML (or a `data.js`), **not** the `.xlsx`. OK? Or do you want to
keep editing spreadsheets and have me re-generate?

**Q7 — Custom domain?** Plain `username.github.io/repo`, or do you have a custom domain
you want it on?

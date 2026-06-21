# Inspiration — Online CV for a Scientist *and* Artist

A research scrapbook of references, layout styles, colour palettes and build
approaches for a personal site that has to carry **both** a serious science record
**and** a body of paintings + writing. Deliberately over-stuffed — **delete the bits
you don't like** and leave me the ones that feel right.

> (The previous version of this file described `artgalleria.com`, a SaaS marketing
> site, which doesn't match a personal online-CV. That's preserved in git history if
> you want it back.)

---

## 0. The core design tension

A science portfolio wants **credibility, density, legibility** (publications, links,
dates). An art portfolio wants **space, mood, image-first restraint**. The whole job
of this site is to hold both without one cheapening the other. The references below
all solve some version of that.

Three ways people resolve it:
1. **One unified gallery aesthetic** — treat papers *and* paintings as "works", same
   card, same calm frame. (Risk: science feels under-stated.)
2. **Two visual registers under one shell** — shared header/colours, but the Science
   page is a tidy catalogue and the Art page is a spacious gallery. (My default rec.)
3. **Split personalities, one bridge** — almost two mini-sites joined by the nav.
   (Most effort; only if the two sides feel truly separate.)

---

## 1. Reference sites & where to look

Personal academic-artist sites are hard to surface by search (they're individuals,
not brands), so the most useful references are **template families** and **categories**
you can browse for the *feel*:

- **al-folio** (Jekyll academic theme) — the gold standard for clean, responsive
  academic sites: auto-generated publications, CV layout, light/dark mode, projects
  grid. Great reference for how to present the **Science** page even though we're
  building static HTML. <https://github.com/alshedivat/al-folio> · live demo:
  <https://alshedivat.github.io/al-folio/>
- **The Fabulous Scientist — Artist Portfolio** — an actual scientist who paints
  (watercolour, "tonalism and impressionism"); good tonal reference for pairing a
  research identity with a painting practice.
  <https://thefabulousscientist.com/my-creations/>
- **Pixpa "30+ Best Artist Portfolio Websites 2026"** — a curated gallery of artist
  sites; skim for layout/mood you like, then tell me which.
  <https://www.pixpa.com/blog/artist-portfolio-websites>
- **CAA Visual-Artist CV conventions** — the standard sections/order for an artist CV
  (useful for the CV page structure). <https://www.collegeart.org/standards-and-guidelines/guidelines/visual-art-cv>
- **Aura — colour schemes for artist websites** — practical palette guidance for
  showing paintings. <https://auraforartists.com/the-best-color-schemes-for-artist-websites/>

**Worth doing together:** browse the Pixpa list and the al-folio demo and just point
at 2–3 you like; I'll match the build to those.

---

## 2. Build-out styles (pick one direction)

Concrete "shapes" the site could take. Each works on phone + laptop.

### Style A — "Gallery catalogue" (my lead recommendation)
- Warm off-white pages, generous margins, paintings on **pure white**.
- Dark-green header band, thin gold hairline dividers between sections.
- Science + Art both use the **same calm card**: image, serif title, italic subtitle,
  expandable text. Feels like a printed exhibition catalogue.
- Best fit for: "classy, Victorian, understated luxury, lets the work speak."

### Style B — "Editorial / literary journal"
- Type-led. Big elegant serif headings, drop-caps on the literature pages, columns of
  running text, sparse imagery. The site reads like a fine small-press magazine.
- Science page becomes a clean reference list; Art page a plated insert.
- Best fit for: leaning into the writing/poetry side as a first-class citizen.

### Style C — "Single-page scroll + section anchors"
- Everything on a long home page; nav scrolls to anchored sections (CV, Science, Art…).
- Modern, app-like, very mobile-friendly. Sub-pages (story pages, CV) still exist.
- Best fit for: fastest to skim on a phone; less "gallery", more "portfolio one-pager".

### Style D — "Framed-plate gallery"
- Each painting sits inside a **rendered frame** (CSS border / passe-partout mat),
  hung on a tinted wall (very subtle green-grey). The CV self-portrait reuses the same
  frame. Strong gallery metaphor.
- Best fit for: maximum "art exhibition" atmosphere; risk of feeling heavy if overdone.

*My pick:* **A as the base, borrowing D's framed self-portrait for the CV**, and B's
drop-caps/serif treatment **only** on the Literature pages.

---

## 3. Colour palettes

You like **dark Victorian green + gold**, with **a little complementary purple**.
That's squarely a "Victorian jewel-tone" palette: deep jewel base + antique neutrals +
one metallic. Anchor with green, accent with gold, season with aubergine.

### Palette 1 — "Hunter green & antique gold" (recommended)
| Role | Hex | Swatch use |
|------|-----|-----------|
| Header / dark green | `#1B3A2B` | header band, footer |
| Deeper green (hover) | `#14342B` | hover, active nav |
| Antique gold | `#C9A24B` | header text, dividers, links |
| Aubergine (rare accent) | `#4B2E4A` | pull-quotes, one-off headings |
| Page background | `#FAF8F4` | warm off-white text pages |
| **Art background** | `#FFFFFF` | **paintings only — true white** |
| Body text | `#1E1E1E` | running text |

### Palette 2 — "Brunswick & brass" (slightly brighter gold)
- Green `#1B4D3E` · gold `#B8860B`/`#CBA135` · plum `#5D3A66` · cream `#F4F1E8`.

### Palette 3 — "Ink base, green hero" (moodier)
- Near-black base `#161714` · emerald hero `#1F5135` · brass `#C9A227` ·
  background `#EFEAE0`. Good if you want a darker, more dramatic site.

**Notes from the research:**
- Victorian palettes = **deep jewel tone + antique neutral + one metal.** Keep
  saturation controlled and use **one** metallic, not several, so it reads modern.
- For showing paintings, the consensus is **neutral/near-white walls** so the artwork
  sets the colour; don't let the site's palette fight the canvases. Hence: dark green
  + gold live in the **chrome** (header, dividers, footer, links); the **canvas wall
  stays white**.
- Reserve **purple for a tiny minority** (hovers, a pull-quote, maybe the Literature
  accent) — it stays special and complements the green without competing with the gold.

### Optional dark mode
A dark mode would invert nicely (deep green-black page, gold text, paintings still on
their own white mats). Easy to add later via CSS variables. Say if you want it.

---

## 4. Typography directions

Fine-art + Victorian → **serif-led**. We'll confirm with the on-page 15-font sampler
(see `plan.md`), but the families cluster into three moods:

- **Refined / fashion-magazine:** Playfair Display, Bodoni Moda, Prata, Italiana —
  high contrast, elegant, great big.
- **Classical / bookish:** EB Garamond, Cormorant Garamond, Cardo, Crimson Pro,
  Libre Baskerville — warm, very readable for the literature pages.
- **Monumental / Victorian titling:** Cinzel, Marcellus — Roman capitals, carved-in-
  stone feel; superb for the "Hamish Patten" wordmark / page titles, paired with a
  calmer body serif.

**Likely winner pattern:** a display face for headings (e.g. Cinzel or Playfair) + a
readable body serif (e.g. EB Garamond or Spectral). Body text could even be a quiet
sans (Inter / Work Sans) if you want science pages to feel crisp — we can A/B it.

---

## 5. Layout & interaction patterns worth stealing

- **Sticky slim header** with the wordmark left, nav right; collapses to a hamburger
  under ~768px. Literature as a dropdown.
- **Expandable work-card**: image, title, italic subtitle, ~30-word teaser, "Read more"
  that expands in place (no page jump). Used identically on Science + Art for cohesion.
- **1-up on phone / 2-up on laptop** card grid (CSS grid, `auto-fit minmax`).
- **Thin gold rule** as section divider instead of heavy boxes.
- **Framed image** component (CSS mat + border) for paintings and the CV portrait.
- **Drop-cap + measured column** for short stories / poems (Style B touch).
- **Subtle scroll-in fade** on sections — keep it gentle; nothing flashy.
- **Lightbox** on paintings (click → full-size on the white wall). Nice-to-have.

---

## 6. Mobile / responsive principles

- Mobile-first CSS; breakpoints ~600px and ~1000px.
- Nav → hamburger; card grids → single column; two-up images → stacked.
- Tap targets ≥44px; images `max-width:100%`; never force horizontal scroll.
- Test the **Visual Art** page hardest on phone — big images, must stay crisp and 1-up.

---

## 7. Build / hosting notes (GitHub Pages)

- Pure **static HTML/CSS/JS** is the safest GitHub-Pages path (no build step).
- If we ever want templating (shared header, auto publication list), **Jekyll** is
  natively supported by GitHub Pages and al-folio shows how far that can go — but it's
  optional and heavier. We can start static and migrate only if upkeep gets annoying.
- Fonts via Google Fonts CDN (or self-host for speed/offline).
- Lightbox/carousel, if used: a tiny dependency-free script, no framework.

---

## 8. Things to decide (cross-ref `plan.md` Open Questions)

- Which **build-out style** (A/B/C/D or a blend)?
- Which **palette** (1/2/3) — and do you want **dark mode**?
- Any **reference sites** from the Pixpa list / al-folio demo you want me to match?
- **Lightbox** on paintings — yes/no?

---

### Sources
- [al-folio Jekyll academic theme (GitHub)](https://github.com/alshedivat/al-folio) · [live demo](https://alshedivat.github.io/al-folio/)
- [The Fabulous Scientist — Artist Portfolio](https://thefabulousscientist.com/my-creations/)
- [Pixpa — 30+ Best Artist Portfolio Websites 2026](https://www.pixpa.com/blog/artist-portfolio-websites)
- [CAA — Visual-Artist CV conventions](https://www.collegeart.org/standards-and-guidelines/guidelines/visual-art-cv)
- [Aura — Best colour schemes for artist websites](https://auraforartists.com/the-best-color-schemes-for-artist-websites/)
- [Media.io — Victorian colour palette ideas + hex](https://www.media.io/color-palette/victorian-color-palette.html)
- [Figma — 100 colour combinations](https://www.figma.com/resource-library/color-combinations/)
- [Piktochart — portfolio colour palettes](https://piktochart.com/blog/portfolio-color-palette/)

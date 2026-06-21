# Design Inspiration — based on artgalleria.com

A reference brief for building a website with a similar look and feel to
[Art Galleria](https://www.artgalleria.com), a clean, professional SaaS marketing
site for art-inventory management software.

> Note: exact brand hex codes and font names are not exposed in the page's
> rendered text. Values below marked _(confirm)_ are recommended approximations
> that reproduce the observed aesthetic — sample the live site's CSS / use a
> browser inspector to lock in the precise values if an exact match is required.

---

## 1. Overall aesthetic & mood

- **Minimalist, light, premium.** Lots of whitespace, high contrast, calm.
- **Enterprise-but-elegant** — trustworthy SaaS, but refined for an art/luxury audience.
- Content-forward: product screenshots and clean icons carry the page, not heavy graphics.
- Tagline tone: short, confident, benefit-led ("Your entire art business, simplified").

---

## 2. Color palette

Predominantly white with dark near-black text and a single accent for CTAs/links.

| Role | Suggested value _(confirm)_ | Usage |
|------|------------------------------|-------|
| Background | `#FFFFFF` | Page background, most sections |
| Alt background | `#F7F8FA` / `#F4F5F7` | Alternating section bands |
| Primary text | `#1A1A1A` / `#212529` | Headings, body |
| Secondary text | `#6B7280` | Sub-copy, captions |
| Accent (brand) | a single teal/blue, e.g. `#0FB5BA` or `#1E6FE0` | Buttons, links, highlights |
| Accent hover | darker shade of accent | Hover/active states |
| Borders / dividers | `#E5E7EB` | Card borders, hairlines |

Keep it to **white + one neutral grey + one accent**. Avoid introducing extra hues.

---

## 3. Typography

- **Family:** clean modern **sans-serif** _(confirm — likely a humanist/geometric grotesk such as Inter, Helvetica Neue, Proxima Nova, or similar)_.
- **Hierarchy:**
  - Hero / display headings: large, ~48–64px, semi-bold.
  - Section headings: ~32–40px, semi-bold.
  - Sub-headings: ~20–24px, medium.
  - Body: ~16–18px, regular, generous line-height (~1.5–1.6).
  - Nav / small labels: ~14–15px, medium.
- High contrast text on white; restrained use of weight (regular + semibold mostly).
- Generous letter spacing on small uppercase labels (optional).

---

## 4. Layout structure

Single-page-style marketing layout, full-width sections stacked vertically, with
content constrained to a centered max-width container (~1140–1280px).

### Header (sticky)
- Logo (left).
- Primary nav (center/right): **Overview · Platform Features ▾ · Integrations · Websites · Contact us**.
  - "Platform Features" is a **dropdown** → For Galleries / For Artists / For Collectors.
- Right side: **Log In** link + a primary CTA button (**Book a Demo** / **Free 14-Day Trial**).
- Stays fixed/sticky on scroll.

### Hero
- Full-width **carousel** with 3 rotating slides, each = headline + supporting image + a "Learn More" link.
- Slide headlines:
  1. "Your entire art business, simplified"
  2. "Designed for galleries, artists, archivists and collection managers"
  3. "Unlimited storage, free upgrades and no hidden fees"

### Audience cards (3-column)
Three cards targeting each segment:
- **For Galleries** — "Manage your complete artwork inventory, artist profiles, contacts, and easily generate invoices, stylish marketing materials and collection catalogs."
- **For Artists** — "Upload, store and manage your artworks on one safe, secure, cloud-based platform."
- **For Collectors** — "Keep your collection data safe, secure and private," with the ability to "privately share selected artworks with invite-only exclusive clients."

### Feature sections (alternating image/text)
Stacked sections, each pairing a product screenshot with a heading + short copy.
Typically alternating left/right image alignment. Headings observed:
- "Elegant, efficient, effective"
- "Art Inventory Software"
- "Database"
- "Invoicing and Sales Reporting"
- "Private Rooms"
- "Easily generate PDF marketing materials"
- "Most integrated arts software"
- "Mobile Apps Included"
- "Apple TV App Included"
- "Other features" (security, speed, support highlights)

### Integrations strip
Row of partner logos:
**Squarespace · Wix · WordPress · WooCommerce · Shopify · QuickBooks · Xero · Mailchimp**

### Footer (multi-column)
- Column: For Galleries · For Artists · For Collectors
- Column: Integrations · Websites · Contact us
- Column: Terms of Service · Privacy & Cookies
- CTA: Book a demo
- International phone numbers + social media icons.

---

## 5. Components / UI patterns to build

- **Sticky nav bar** with dropdown mega/sub-menu.
- **Hero carousel/slider** (autoplay, 3 slides, dots or arrows).
- **Feature card** (icon/screenshot + title + 1–2 line description).
- **Alternating media+text rows** (image left/right toggle).
- **Logo cloud / integrations strip**.
- **Primary & secondary buttons.**
- **Multi-column footer.**

---

## 6. Buttons & CTAs

- **Primary button:** solid accent fill, white text, rounded corners (~4–8px radius), medium padding. Used for "Book a Demo", "Free 14-Day Trial".
- **Secondary / text link:** "Learn More" inline links in accent color.
- Clear contrast; CTAs repeated throughout the page.

---

## 7. Spacing & rhythm

- Generous vertical padding between sections (~80–120px top/bottom on desktop).
- Comfortable gutters; content max-width centered.
- Whitespace is a core design element — don't crowd.

---

## 8. Imagery style

- Polished **product screenshots** (app/dashboard UI) framed cleanly.
- Simple **line/flat icons** for features.
- High-quality artwork imagery in hero/private-rooms context.
- Consistent, professional, uncluttered.

---

## 9. Interactions / animation

- Hero carousel auto-rotation + manual controls.
- Subtle hover states on buttons, links, and cards (color shift / slight lift).
- Likely gentle fade/slide-in on scroll for sections (optional, keep subtle).
- Sticky header behavior on scroll.

---

## 10. Suggested tech stack (to recreate)

- **HTML/CSS** with a utility framework (Tailwind CSS) or plain CSS with a design-token setup (CSS variables for the palette above).
- **Carousel:** Swiper.js or a lightweight slider.
- **Responsive:** mobile-first; nav collapses to a hamburger menu < ~768px; multi-column grids stack to single column.
- Optional: React/Next.js or Astro for componentized sections; or a static site if simple.
- Fonts via Google Fonts / self-hosted (e.g. Inter) _(confirm)_.

---

## 11. Build checklist

- [ ] Define design tokens (colors, type scale, spacing) as CSS variables.
- [ ] Sticky responsive header with dropdown + mobile menu.
- [ ] Hero carousel (3 slides).
- [ ] 3-up audience cards.
- [ ] Reusable alternating media+text section component.
- [ ] Integrations logo strip.
- [ ] Multi-column responsive footer.
- [ ] Primary/secondary button styles + hover states.
- [ ] Responsive breakpoints + scroll/hover animations.

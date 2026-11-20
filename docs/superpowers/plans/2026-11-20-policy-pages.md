# Policy pages v1 Implementation Plan

> **For agentic workers:** Execution method chosen by owner: Claude leads, `agy` writes the code from briefs in `.agy/`, Claude reviews and verifies. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Static Privacy Policy + Terms of Service pages for Anluti Mall, Vietnamese and English, deployable to `policy.anlutimall.shop`.

**Architecture:** Hand-written HTML, one shared `assets/style.css`, no JS required for content, no build step, no dependencies. One URL per page per language, linked with relative paths so the site works on any static host and from `file://`.

**Tech Stack:** HTML5, CSS (custom properties, `backdrop-filter`), Python 3 stdlib for the check script.

**Spec:** `docs/superpowers/specs/2026-11-20-policy-pages-design.md`

## Global Constraints

- Files: `index.html`, `404.html`, `privacy/index.html`, `terms/index.html`, `en/privacy/index.html`, `en/terms/index.html`, `assets/style.css`, `assets/favicon.svg`.
- All internal links relative (`../terms/`, `../../privacy/`), never root-absolute.
- Contact email everywhere: `support@anlutimall.shop`. Brand: `Anluti Mall`. No legal entity, address, phone, tax ID.
- Effective date: VI `20/11/2026`, EN `20 November 2026`, plus `<time datetime="2026-11-20">`.
- Retention: account data kept while the account is active; deleted within 30 days of an emailed request.
- Third parties named exactly: Google (sign-in), Cloudflare R2 (image storage), Resend (email). Never name Cloudinary or Supabase.
- No filler sentences, no "we value your privacy", no dev notes, no placeholders, no lorem.
- Design: light glass panels on a warm soft background, dark mode via `prefers-color-scheme`, no violet/lavender, WCAG AA contrast, visible focus ring, links/buttons outside running text ≥ 44px tall, hover states on every link/button, `prefers-reduced-motion` respected, works at 320px wide with no horizontal scroll.
- Each page: `<html lang="vi|en">`, `<title>`, `<meta name="description">`, viewport meta, `<link rel="alternate" hreflang>` for vi, en, x-default (= vi), `<link rel="canonical">` to `https://policy.anlutimall.shop/...`.

## Review Focus

1. Section ids differ between VI and EN pages → language switch lands on a different section. `check.py` asserts identical section-id lists per VI/EN pair.
2. A TOC link points at a missing id → dead jump. `check.py` asserts every `#id` href resolves.
3. Relative link depth wrong in `en/` pages (`../` vs `../../`) → 404 on the language switch. `check.py` resolves every relative href to a file.
4. Long email / words overflow at 320px. Claude checks with a 320px screenshot.
5. Dark mode text on glass below contrast. Claude checks both schemes by screenshot.

---

### Task 1: Check script (Claude)

**Files:** Create `scripts/check.py`, `.gitignore` (contains `.agy/`).

- [ ] `python scripts/check.py` exits 1 on empty repo (pages missing), prints each failure.
- [ ] Asserts per page: file exists; `lang` correct; title, description, viewport, canonical, 3 hreflang links present; stylesheet linked; every relative href resolves to an existing file (dir → `index.html`); every `#id` href resolves; email present on the 4 policy pages; date `2026-11-20` present on the 4 policy pages; forbidden strings absent (`TODO`, `lorem`, `Lorem`, `placeholder`, `{{`, `example.com`, `Cloudinary`, `Supabase`).
- [ ] Asserts VI/EN pairs have identical ordered lists of `<section id>`.
- [ ] Commit `chore(repo): add page check script`.

### Task 2: Style + Vietnamese pages (agy, brief `.agy/brief-1.md`)

**Files:** Create `assets/style.css`, `assets/favicon.svg`, `privacy/index.html`, `terms/index.html`, `index.html` (redirect to `privacy/`), `404.html`.

**Produces (Task 3 relies on):** markup skeleton and class names; section ids:
- privacy: `who`, `data`, `use`, `third-parties`, `browser-storage`, `retention`, `rights`, `changes`
- terms: `service`, `accounts`, `acceptable-use`, `orders`, `content`, `liability`, `changes`, `contact`

- [ ] agy writes files per brief.
- [ ] `python scripts/check.py` → only EN-page failures remain.
- [ ] `node <taste>/scripts/copy-lint.mjs privacy/index.html terms/index.html --kind service` → no FAIL (WARNs reviewed).
- [ ] Claude screenshots 1440 / 390 / 320, light + dark; fixes or re-briefs.
- [ ] Commit `feat(pages): add vietnamese privacy and terms pages`.

### Task 3: English pages (agy, brief `.agy/brief-2.md`)

**Files:** Create `en/privacy/index.html`, `en/terms/index.html`.

**Consumes:** Task 2 markup and section ids, copied 1:1, text translated naturally (not word-for-word).

- [ ] agy writes files per brief.
- [ ] `python scripts/check.py` → `ALL CHECKS PASSED`, exit 0.
- [ ] copy-lint on EN pages → no FAIL.
- [ ] Claude screenshots EN at 390; clicks language switch both ways.
- [ ] Commit `feat(pages): add english privacy and terms pages`.

### Task 4: README (Claude)

- [ ] `README.md`: what the repo is, page URLs, how to preview (`python -m http.server`), how to check (`python scripts/check.py`), deploy note (static host, custom domain `policy.anlutimall.shop`, Google Branding links).
- [ ] Commit `docs(repo): add readme`.

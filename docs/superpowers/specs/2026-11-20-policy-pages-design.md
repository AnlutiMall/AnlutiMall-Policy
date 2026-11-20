# Policy pages (privacy + terms), v1 — design

Date: 2026-11-20 · Status: draft, awaiting owner approval

## Intent

Anluti Mall (plush/toy shop: customer storefront, admin/staff inventory app) needs
public Privacy Policy and Terms of Service pages so the Google OAuth consent screen
can be published (Branding page requires home page + privacy + terms links on the
authorized domain `anlutimall.shop`). Start simple, improve over time.

## Goals

- Privacy Policy and Terms of Service, each in Vietnamese and English.
- Content matches what the system actually does today — nothing invented.
- Looks polished (light glass style), easy to read on phone and desktop.
- Static files: deployable to any static host on `policy.anlutimall.shop`.

## Non-goals (v1)

- Return / shipping / payment policies (required later by VN e-commerce rules
  once online checkout exists).
- Cookie banner, analytics, CMS, search.
- Legal entity details (business name, tax ID, address, phone) — not decided yet.

## Anti-goals

- Filler text no reader needs ("We truly value your privacy…", AI-sounding intros).
- Claims the system doesn't back (e.g. self-service account deletion, data
  location, certifications).
- Leftover dev notes / placeholders visible on the page.

## Facts the content is built on (from the code, 2026-11-20)

- Account data stored: full name, email, avatar image, password (hashed, only for
  email sign-up), Google account ID (Google sign-in), email-verified flag, last
  login time, created/updated time.
- Google sign-in requests only basic profile: `openid`, `email`, `profile`.
- Third parties: Google (sign-in), Cloudflare R2 (image storage — replaces
  Cloudinary), Resend (transactional email: verification, password reset).
- Browser storage: sign-in session and cart/wishlist kept in the browser's local
  storage. No advertising or analytics trackers.
- Users cannot delete their own account in the app; deletion is done by the shop
  on request.
- Contact: `support@anlutimall.shop` (owner-provided).

## Approaches considered

1. **Hand-written static HTML + one CSS file (chosen).** One URL per page per
   language, no build step, no dependencies. Fastest to load, trivial to host,
   crawlers read every language.
2. Astro / Next.js site — rejected: framework weight for four text pages.
3. Single page with JS language toggle — rejected: English content may be
   invisible to crawlers and to Google's reviewer without JS.

## Design

Structure:

```
index.html            -> redirects/links to /privacy/ (vi)
privacy/index.html    (vi)      terms/index.html    (vi)
en/privacy/index.html (en)      en/terms/index.html (en)
assets/style.css      assets/logo (owner's penguin logo, if provided)
404.html
```

Page layout (same on all four): header (brand + VI/EN switch + Privacy/Terms
links) · title + "effective date" · table of contents (sticky on desktop) ·
numbered sections · footer (contact email, © Anluti Mall).

Privacy sections: 1 Who we are & contact · 2 Data we collect · 3 How we use it ·
4 Third parties · 5 Browser storage · 6 Retention & deletion · 7 Your rights ·
8 Changes to this policy.

Terms sections: 1 About the service · 2 Accounts · 3 Acceptable use ·
4 Products, prices & orders (brief; detailed policies later) · 5 Content &
images · 6 Limitation of liability · 7 Changes · 8 Contact.

Visual: design via `design-taste-frontend` skill; glass panels on a soft
background, system font stack with Vietnamese support, `prefers-color-scheme`
dark mode, WCAG AA contrast, no external requests except optional Google Font.

## Calls made by Claude (owner can override)

- Brand shown as "Anluti Mall"; no legal entity named yet.
- Effective date 2026-11-20.
- Retention: account data kept while the account is active; deleted within
  **30 days** of an emailed request. ← needs owner confirmation.
- Hosting target `policy.anlutimall.shop`; host choice (Cloudflare Pages vs
  GitHub Pages) left to owner — files work on both.
- Coding delegated to agy subagent; review + verification by Claude.

## Left to the builder

Exact wording within the facts above, CSS details, logo placement.

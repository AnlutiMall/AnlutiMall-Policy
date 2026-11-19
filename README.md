# AnlutiMall-Policy

Static Privacy Policy and Terms of Service pages for Anluti Mall, in Vietnamese and English.
Plain HTML + one CSS file: no build step, no dependencies.

## Pages

| Page | Vietnamese | English |
|---|---|---|
| Privacy Policy | `/privacy/` | `/en/privacy/` |
| Terms of Service | `/terms/` | `/en/terms/` |

`/` redirects to `/privacy/`. Production URL: `https://policy.anlutimall.shop/`.

## Preview

```bash
python -m http.server 8000
# open http://localhost:8000/privacy/
```

## Check before committing

```bash
python scripts/check.py
```

Verifies every page exists, has the right `lang`, title, description, canonical and
hreflang links, that every relative link and `#anchor` resolves, that VI and EN pages
share the same section ids, and that no placeholder text is left.

## Editing

- Change the text in both languages in the same commit, and keep section ids identical.
- When the policy changes, update the effective date (`<time datetime>`) on every changed page.
- Links between pages are relative (`../terms/`), never root-absolute.

## Deploy

Any static host works (Cloudflare Pages or GitHub Pages): publish the repo root,
set the custom domain `policy.anlutimall.shop`, enforce HTTPS.

Google OAuth consent screen → Branding:

- Application home page: `https://anlutimall.shop`
- Privacy policy: `https://policy.anlutimall.shop/privacy/`
- Terms of service: `https://policy.anlutimall.shop/terms/`

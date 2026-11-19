"""Static checks for the policy pages. Run: python scripts/check.py"""
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://policy.anlutimall.shop/"
EMAIL = "congdinh.dev@gmail.com"
FORBIDDEN = ["TODO", "lorem", "Lorem", "placeholder", "{{", "example.com", "Cloudinary", "Supabase"]

# path -> (lang, canonical path, counterpart path)
PAGES = {
    "privacy/index.html": ("vi", "privacy/", "en/privacy/index.html"),
    "terms/index.html": ("vi", "terms/", "en/terms/index.html"),
    "en/privacy/index.html": ("en", "en/privacy/", "privacy/index.html"),
    "en/terms/index.html": ("en", "en/terms/", "terms/index.html"),
}
EXTRA = ["index.html", "404.html", "assets/style.css", "assets/favicon.svg"]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.title = False
        self.metas = {}
        self.links = []  # (rel, href, hreflang)
        self.hrefs = []
        self.ids = set()
        self.section_ids = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self.title = True
        elif tag == "meta" and "name" in a:
            self.metas[a["name"]] = a.get("content", "")
        elif tag == "link":
            self.links.append((a.get("rel", ""), a.get("href", ""), a.get("hreflang")))
        elif tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        elif tag == "section" and "id" in a:
            self.section_ids.append(a["id"])


def parse(rel):
    p = Page()
    p.feed((ROOT / rel).read_text(encoding="utf-8"))
    return p


def resolve(page_rel, href):
    target = (ROOT / page_rel).parent / href.split("#")[0]
    return target / "index.html" if href.split("#")[0].endswith("/") or target.is_dir() else target


def check_page(rel, errors):
    text = (ROOT / rel).read_text(encoding="utf-8")
    p = parse(rel)
    for bad in FORBIDDEN:
        if bad in text:
            errors.append(f"{rel}: forbidden string {bad!r}")
    for href in p.hrefs + [h for _, h, _ in p.links]:
        if href.startswith(("http:", "https:", "mailto:")):
            continue
        if href.startswith("#"):
            if href[1:] and href[1:] not in p.ids:
                errors.append(f"{rel}: anchor {href} has no matching id")
        elif href.startswith("/"):
            errors.append(f"{rel}: root-absolute link {href} (use relative)")
        elif not resolve(rel, href).exists():
            errors.append(f"{rel}: link {href} does not resolve")
    return p, text


def main():
    errors = []
    for rel in EXTRA:
        if not (ROOT / rel).exists():
            errors.append(f"missing {rel}")
    for rel in ("index.html", "404.html"):
        if (ROOT / rel).exists():
            check_page(rel, errors)

    parsed = {}
    for rel, (lang, canon, other) in PAGES.items():
        if not (ROOT / rel).exists():
            errors.append(f"missing {rel}")
            continue
        p, text = check_page(rel, errors)
        parsed[rel] = p
        if p.lang != lang:
            errors.append(f"{rel}: lang={p.lang!r}, expected {lang!r}")
        if not p.title:
            errors.append(f"{rel}: no <title>")
        for name in ("description", "viewport"):
            if not p.metas.get(name):
                errors.append(f"{rel}: missing meta {name}")
        rels = {(r, h, l) for r, h, l in p.links}
        if not any(r == "canonical" and h == BASE + canon for r, h, _ in rels):
            errors.append(f"{rel}: canonical must be {BASE + canon}")
        vi_canon = canon[3:] if lang == "en" else canon
        want = {"vi": BASE + vi_canon, "en": BASE + "en/" + vi_canon, "x-default": BASE + vi_canon}
        for hl, url in want.items():
            if ("alternate", url, hl) not in rels:
                errors.append(f"{rel}: missing hreflang {hl} -> {url}")
        if not any(r == "stylesheet" for r, _, _ in rels):
            errors.append(f"{rel}: no stylesheet")
        if EMAIL not in text:
            errors.append(f"{rel}: contact email missing")
        if "2026-11-20" not in text:
            errors.append(f"{rel}: effective date 2026-11-20 missing")
        if not p.section_ids:
            errors.append(f"{rel}: no <section id> elements")

    for rel, (lang, _, other) in PAGES.items():
        if lang == "vi" and rel in parsed and other in parsed:
            if parsed[rel].section_ids != parsed[other].section_ids:
                errors.append(f"{rel} vs {other}: section ids differ "
                              f"{parsed[rel].section_ids} != {parsed[other].section_ids}")

    for e in errors:
        print("FAIL", e)
    print("ALL CHECKS PASSED" if not errors else f"{len(errors)} failure(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

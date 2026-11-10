#!/usr/bin/env python3
"""Build all supported language versions as plain GitHub Pages files."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sitegen"
BASE = "https://taro.mom"
ENTRIES = (
    "https://t.me/taroshenka_bot?start=ref974025936",
    "https://t.me/astrology_1_bot?start=ref974025936",
    "https://app.taro.mom/?ref=974025936",
)
OLD_ROUTES = ("home", "daily-card", "yes-no", "three-card", "relationships")
ASTRO_ROUTES = ("astro", "natal", "compatibility", "horoscopes", "transits", "solar", "moon")
ROUTES = json.loads((SOURCE / "routes.json").read_text())
LOCALES = json.loads((SOURCE / "locales.json").read_text())
REVISION = json.loads((SOURCE / "revision.json").read_text())
LOCALE_BY_CODE = {x["code"]: x for x in LOCALES}
VISUAL_THEMES = json.loads((SOURCE / "visual-themes.json").read_text())
TOPIC_ICONS = {
    "home": "cards", "daily-card": "daily_card", "yes-no": "spread_yesno",
    "three-card": "spread_3cards", "relationships": "spread_relationship",
    "astro": "star", "natal": "astro_natal", "compatibility": "astro_synastry",
    "horoscopes": "astro_today", "transits": "astro_transits",
    "solar": "astro_solar", "moon": "astro_moon",
}
SECTION_ICONS = {
    "home": ("sparkle", "cards", "book", "coin"),
    "daily-card": ("daily_card", "telegram", "message"),
    "yes-no": ("message", "spread_yesno", "telegram"),
    "three-card": ("spread_3cards", "message", "book"),
    "relationships": ("message", "spread_relationship", "cards"),
    "astro": ("star", "user", "globe"),
    "natal": ("astro_natal", "user", "shield"),
    "compatibility": ("astro_synastry", "user", "cards"),
    "horoscopes": ("astro_today", "book", "shield"),
    "transits": ("astro_transits", "astro_events", "pen"),
    "solar": ("astro_solar", "user", "star"),
    "moon": ("astro_moon", "pen", "user"),
}


def icon(name, css=""):
    return f'<svg class="pictogram {css}" width="24" height="24" viewBox="0 0 24 24" stroke-width="1.8" aria-hidden="true" focusable="false"><use href="/sitegen/assets/icons.svg#{name}"></use></svg>'


def esc(value):
    return html.escape(str(value), quote=True)


def path(code, key):
    if key in ASTRO_ROUTES:
        route = ROUTES[key]
        if code in route["paths"]:
            return route["paths"][code]
        stem = LOCALE_BY_CODE[code]["homePath"].rstrip("/") + "/astro/"
        return stem if key == "astro" else stem + route["englishSlug"] + "/"
    loc = next(x for x in LOCALES if x["code"] == code)
    if key == "home":
        return loc["homePath"]
    slug = ROUTES[key]["slugs"].get(code, ROUTES[key]["englishSlug"])
    return f'/{"en" if code == "en" else loc["publicSegment"]}/{slug}/'


def alternates(key):
    return [(x["hreflang"], BASE + path(x["code"], key)) for x in LOCALES] + [("x-default", BASE + path("en", key))]


def language_links(code, key):
    return "".join(f'<a href="{path(x["code"], key)}" lang="{x["hreflang"]}" hreflang="{x["hreflang"]}" dir="{x["dir"]}"' + (' aria-current="page"' if x["code"] == code else '') + f'>{esc(x["nativeLabel"])}</a>' for x in LOCALES)


def entry_block(ui):
    items = []
    for i, (url, label, note) in enumerate(zip(ENTRIES, ui["entry_labels"], ui["entry_notes"]), 1):
        symbol = ("telegram", "star", "globe")[i - 1]
        items.append(f'<li><a class="entry-link entry-{i}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{icon(symbol, "entry-icon")}<span>{esc(label)}</span><span aria-hidden="true">↗</span></a><small>{esc(note)}</small></li>')
    return f'<ol class="entry-list" aria-label="{esc(ui["entry_heading"])}">' + "".join(items) + '</ol>'


def paragraph(text):
    return f"<p>{esc(text)}</p>"


def section(block, index, symbol, extra=""):
    heading = block["heading"]
    body = "".join(paragraph(x) for x in block.get("paragraphs", []))
    if block.get("items"):
        body += '<ul class="text-list">' + "".join(f"<li>{esc(x)}</li>" for x in block["items"]) + "</ul>"
    return f'<section class="copy-section" aria-labelledby="section-{index}"><div class="section-title">{icon(symbol)}<h2 id="section-{index}">{esc(heading)}</h2></div>{extra}{body}</section>'


def horoscope_formats(code):
    cards = []
    for item in VISUAL_THEMES[code]["formats"]:
        cards.append(f'<article class="horoscope-format format-{item["key"]}"><img src="/images/en/{item["image"]}" width="960" height="960" alt="" aria-hidden="true" loading="lazy"><div class="format-copy"><h3>{esc(item["heading"])}</h3><p>{esc(item["text"])}</p></div></article>')
    return '<div class="horoscope-formats">' + "".join(cards) + '</div>'


def topic_cards(data, code, keys):
    return '<div class="topic-grid">' + "".join(f'<a class="topic-card" href="{path(code, key)}"><div class="topic-card-heading">{icon(TOPIC_ICONS[key], "topic-icon")}<span class="topic-type">{esc(data["pages"][key]["eyebrow"])}</span></div><h3>{esc(data["pages"][key]["h1"])}</h3><p>{esc(data["pages"][key]["card_text"])}</p><span class="text-link">{esc(data["ui"]["explore"])} <span aria-hidden="true">↗</span></span></a>' for key in keys) + "</div>"


def product_image(ui, code, kind, caption=None):
    dimensions = {"tarot": (780, 1160), "card": (780, 1160), "astro": (780, 1160)}
    width, height = dimensions[kind]
    image = f'/images/en/app-{kind}-{code}.webp'
    return f'<figure class="product-figure"><img src="{image}" width="{width}" height="{height}" alt="{esc(ui["image_alt"][kind])}" loading="lazy"><figcaption>{esc(caption or ui["example_caption"])}</figcaption></figure>'


def graph(data, code, key, page):
    canonical = BASE + path(code, key)
    actions = [{"@type": "ViewAction", "name": label, "target": url} for label, url in zip(data["ui"]["entry_labels"], ENTRIES)]
    return json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": data["ui"]["brand"], "inLanguage": [x["hreflang"] for x in LOCALES]},
        {"@type": "SoftwareApplication", "@id": BASE + "/#application", "name": data["ui"]["brand"], "url": BASE + "/", "sameAs": ["https://t.me/taroshenka_bot", "https://t.me/astrology_1_bot"], "applicationCategory": "EntertainmentApplication", "operatingSystem": "Telegram, Web browser", "description": data["ui"]["entity_description"], "potentialAction": actions},
        {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": page["title"], "description": page["description"], "inLanguage": LOCALE_BY_CODE[code]["hreflang"], "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": BASE + "/#application"}, "potentialAction": actions},
    ]}, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


def render(data, code, key):
    ui = data["ui"]
    page = data["pages"][key]
    astro = key in ASTRO_ROUTES
    themed = code in VISUAL_THEMES and key in ("natal", "horoscopes")
    canonical = BASE + path(code, key)
    hrefs = "\n".join(f'<link rel="alternate" hreflang="{lang}" href="{url}">' for lang, url in alternates(key))
    home = path(code, "home")
    loc = LOCALE_BY_CODE[code]
    breadcrumbs = ""
    if key != "home":
        trail = f'<a href="{home}">{esc(ui["home"])}</a><span aria-hidden="true">/</span>'
        if astro and key != "astro":
            trail += f'<a href="{path(code, "astro")}">{esc(ui["astro"])}</a><span aria-hidden="true">/</span>'
        breadcrumbs = f'<nav class="breadcrumbs" aria-label="{esc(ui["breadcrumbs"])}">{trail}<span>{esc(page["h1"])}</span></nav>'
    hero_media = f'<picture class="hero-art"><source type="image/webp" srcset="/images/en/tarot-reader-hero.webp"><img src="/images/en/tarot-reader-hero-desktop.jpg" width="1600" height="900" alt="{esc(ui["hero_alt"])}" fetchpriority="high"></picture>'
    if key != "home":
        hero_media = f'<div class="topic-emblem" aria-hidden="true">{icon(TOPIC_ICONS[key])}</div>'
    if themed:
        artwork = "astro-natal-wheel.svg" if key == "natal" else "astro-love-pair.svg"
        hero_media = f'<div class="theme-art" aria-hidden="true"><img src="/images/en/{artwork}" width="960" height="960" alt="" fetchpriority="high"></div>'
    body = "".join(section(x, i, SECTION_ICONS[key][i - 1], horoscope_formats(code) if themed and key == "horoscopes" and i == 1 else "") for i, x in enumerate(page["sections"], 1))
    if key == "home":
        body = f'<section class="catalog section-space" id="readings"><div class="section-heading"><span class="eyebrow">{esc(ui["tarot"])}</span><h2>{esc(ui["tarot_heading"])}</h2><p>{esc(ui["tarot_intro"])}</p></div>{topic_cards(data, code, OLD_ROUTES[1:])}</section>' + body
    if key in ("home", "astro"):
        body += f'<section class="section-space" id="astro-topics"><div class="section-heading"><span class="eyebrow">{esc(ui["astro"])}</span><h2>{esc(ui["astro_heading"])}</h2><p>{esc(ui["astro_intro"])}</p></div>{topic_cards(data, code, ASTRO_ROUTES[1:])}</section>'
    image_kind = "astro" if astro else ("card" if key in ("daily-card", "yes-no") else "tarot")
    sample = f'<section class="product-section section-space"><div class="product-copy"><span class="eyebrow">{esc(ui["inside"])}</span><h2>{esc(page.get("example_heading", ui["example_heading"]))}</h2><p>{esc(page.get("example_text", ui["example_text"]))}</p><p>{esc(ui["account_text"])}</p><a class="text-link" href="{path(code, "astro") if not astro else home}">{esc(ui["cross_link_astro"] if not astro else ui["cross_link_tarot"])} →</a></div>{product_image(ui, code, image_kind)}</section>'
    faq = f'<section class="faq section-space" id="faq"><div class="section-heading"><span class="eyebrow">{esc(ui["answers"])}</span><h2>{esc(ui["faq"])}</h2></div>' + "".join(f'<details open><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in page["faq"]) + "</section>"
    related = page.get("related", [])
    if related:
        body += f'<section class="section-space related"><h2>{esc(ui["related"])}</h2><div class="related-links">' + "".join(f'<a href="{path(code, k)}">{esc(data["pages"][k]["h1"])} <span aria-hidden="true">↗</span></a>' for k in related) + "</div></section>"
    all_languages = language_links(code, key)
    languages = f'<details class="language-directory"><summary>{esc(ui["other_languages"])}</summary><p>{esc(ui["other_languages_note"])}</p><div class="language-links">{all_languages}</div></details>'
    values = {
        "lang": loc["hreflang"], "dir": loc["dir"], "title": esc(page["title"]), "description": esc(page["description"]), "canonical": canonical, "hreflang": hrefs,
        "og_locale": loc["ogLocale"], "jsonld": graph(data, code, key, page), "skip": esc(ui["skip"]), "home_path": home,
        "brand": esc(ui["brand"]), "home": esc(ui["home"]), "tarot": esc(ui["tarot"]), "astro": esc(ui["astro"]), "faq_label": esc(ui["faq"]), "astro_path": path(code, "astro"),
        "locale_label": esc(loc["nativeLabel"]), "locale_links": all_languages, "switch_label": esc(ui["switch_language"]), "language_icon": icon("globe"),
        "breadcrumbs": breadcrumbs, "eyebrow": esc(page["eyebrow"]), "h1": esc(page["h1"]), "lead": esc(page["lead"]), "entries": entry_block(ui), "hero_media": hero_media,
        "body": body, "sample": sample, "faq": faq, "final_title": esc(ui["final_title"]), "final_text": esc(ui["final_text"]), "disclaimer_title": esc(ui["disclaimer_title"]),
        "disclaimer": esc(ui["disclaimer"]), "astro_disclaimer": paragraph(ui["astro_disclaimer"]) if astro else "", "support": esc(ui["support"]), "languages": languages,
        "attribution_note": esc(ui["attribution_note"]),
        "brand_icon": icon("sparkle"), "page_key": key,
        "theme_styles": '\n<link rel="stylesheet" href="/sitegen/assets/astro-themes.css">' if themed else "",
        "theme_class": " theme-astro" if themed else "",
        "nav_styles": '\n<link rel="stylesheet" href="/sitegen/assets/navigation-buttons.css">',
    }
    raw = (SOURCE / "templates/product.html").read_text()
    for name, value in values.items():
        raw = raw.replace("{{" + name + "}}", value)
    if re.search(r"\{\{[a-z_]+\}\}", raw):
        raise ValueError("unresolved template placeholder")
    return raw


def outputs():
    out = {}
    for code in REVISION["locales"]:
        data = json.loads((SOURCE / "content" / f"{code}.json").read_text())
        if data.get("revision") != REVISION["id"]:
            raise ValueError(f"unsupported content revision: {code}")
        for key in (*OLD_ROUTES, *ASTRO_ROUTES):
            out[path(code, key)] = render(data, code, key)
    return out


def update_sitemap(routes):
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    xns = "http://www.w3.org/1999/xhtml"
    ET.register_namespace("", ns)
    ET.register_namespace("xhtml", xns)
    target = ROOT / "sitemap.xml"
    tree = ET.parse(target)
    root = tree.getroot()
    rows = {row.findtext(f"{{{ns}}}loc"): row for row in root}
    reverse = {BASE + path(code, key): key for code in REVISION["locales"] for key in (*OLD_ROUTES, *ASTRO_ROUTES)}
    for route in routes:
        canonical = BASE + route
        row = rows.get(canonical)
        if row is None:
            row = ET.SubElement(root, f"{{{ns}}}url")
            ET.SubElement(row, f"{{{ns}}}loc").text = canonical
        lastmod = row.find(f"{{{ns}}}lastmod")
        if lastmod is None:
            lastmod = ET.SubElement(row, f"{{{ns}}}lastmod")
        lastmod.text = REVISION["updated"]
        for old in list(row.findall(f"{{{xns}}}link")):
            row.remove(old)
        for lang, url in alternates(reverse[canonical]):
            ET.SubElement(row, f"{{{xns}}}link", {"rel": "alternate", "hreflang": lang, "href": url})
    ET.indent(tree, space="  ")
    tree.write(target, encoding="UTF-8", xml_declaration=True)
    with target.open("a") as handle:
        handle.write("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generated = outputs()
    errors = []
    for route, raw in generated.items():
        dest = ROOT / route.strip("/") / "index.html"
        if args.check:
            if not dest.is_file() or dest.read_text() != raw:
                errors.append(route)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(raw)
    if errors:
        raise SystemExit("Stale generated pages: " + ", ".join(errors))
    if not args.check:
        update_sitemap(generated)
    print(json.dumps({"revision": REVISION["id"], "pages": len(generated), "check": args.check}))


if __name__ == "__main__":
    main()

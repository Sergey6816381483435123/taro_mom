# Verification report: expand-site-to-20-locales

Date: 2026-08-13  
Baseline branch: `main`  
Baseline commit: `ae75039434661a01602de53483d33dbe48d13a81`  
Schema: `spec-driven`

## Scope and baseline

The implementation uses the confirmed contract of exactly 20 locales, five route keys, and four Premium readings. The baseline contained 16 canonical HTML pages (eight locale homes and four English/Russian detail pairs) plus the non-canonical `/en/` home redirect. The existing `CNAME` remains `taro.mom`. The user-owned handoff file was not modified. Existing user changes in `taro-bot-website-master-description.md` were preserved.

Five route keys are implemented: `home`, `daily-card`, `yes-no`, `three-card`, and `relationships`. Dawn and Premium readings remain content/catalog entries, not additional detail routes.

Live PostgreSQL/n8n access was not available from this repository. The live bot catalog was not verified; the user-confirmed product contract was used. No bot, n8n, PostgreSQL, payment catalog, or external service was changed.

## Commands and tool versions

```text
Python 3.13.0
OpenSpec 1.6.0
Git 2.51.0.windows.1
python tools/create_locale_content.py
python tools/generate_site.py
python tools/generate_site.py --check
python tools/test_sitegen.py
python tools/check_site.py
python tools/http_smoke.py
python tools/visual_smoke.py
openspec.cmd validate expand-site-to-20-locales --strict
git diff --check
```

All commands above completed successfully. `git diff --check` was clean; Git's Windows line-ending notices are not whitespace errors.

## Generated counts and locale matrix

| Code | Native label | Direction | Home | Detail routes | Metadata/schema | Missing | Blank | Link/HTTP result |
|---|---|---:|---:|---:|---:|---:|---:|---|
| en | English | ltr | 1 | 4 | pass | 0 | 0 | pass |
| ru | Русский | ltr | 1 | 4 | pass | 0 | 0 | pass |
| id | Bahasa Indonesia | ltr | 1 | 4 | pass | 0 | 0 | pass |
| ms | Bahasa Melayu | ltr | 1 | 4 | pass | 0 | 0 | pass |
| de | Deutsch | ltr | 1 | 4 | pass | 0 | 0 | pass |
| es | Español | ltr | 1 | 4 | pass | 0 | 0 | pass |
| fr | Français | ltr | 1 | 4 | pass | 0 | 0 | pass |
| it | Italiano | ltr | 1 | 4 | pass | 0 | 0 | pass |
| nl | Nederlands | ltr | 1 | 4 | pass | 0 | 0 | pass |
| uz | Oʻzbek | ltr | 1 | 4 | pass | 0 | 0 | pass |
| pl | Polski | ltr | 1 | 4 | pass | 0 | 0 | pass |
| pt | Português (Brasil) | ltr | 1 | 4 | pass | 0 | 0 | pass |
| tr | Türkçe | ltr | 1 | 4 | pass | 0 | 0 | pass |
| be | Беларуская | ltr | 1 | 4 | pass | 0 | 0 | pass |
| uk | Українська | ltr | 1 | 4 | pass | 0 | 0 | pass |
| kk | Қазақша | ltr | 1 | 4 | pass | 0 | 0 | pass |
| ar | العربية | rtl | 1 | 4 | pass | 0 | 0 | pass |
| fa | فارسی | rtl | 1 | 4 | pass | 0 | 0 | pass |
| ko | 한국어 | ltr | 1 | 4 | pass | 0 | 0 | pass |
| hi | हिन्दी | ltr | 1 | 4 | pass | 0 | 0 | pass |

Totals: 20 home pages + 80 detail pages = 100 canonical pages, plus exactly one `/en/` home redirect = 101 HTML documents. `sitemap.xml` contains exactly 100 `<loc>` values and 2,100 alternate links (21 per canonical URL: 20 locales plus `x-default`).

## Locally verified

- Locale normalization: base tags, `pt-BR` to `pt`, blank/`NULL`/disabled/unknown to `en`, and diagnostic `requested -> en -> ru` fallback.
- Exact route construction, including existing English/Russian detail slugs and `/pt-br/`.
- Strict dictionary parity, types, nonblank values, placeholders, and negative fixtures for missing, blank, extra, wrong-type, and placeholder errors.
- Deterministic generation and drift check: `generated=105 changed=0`.
- Self-canonical URLs, 20 reciprocal `hreflang` entries, route-equivalent `x-default`, `lang`, `dir`, Open Graph, Twitter metadata, and JSON-LD parsing.
- Exact conversion CTA: `https://t.me/taroshenka_bot?start=ref974025936`; new-tab links use `rel="noopener noreferrer"`. Plain identity URL and username are checked separately.
- Premium card counts 7/7/10/12, 20-language catalog, credits/payment copy variants, disclaimer keys, and route/product catalog shape.
- Publishable forbidden-content scan: no `Visconti`, public `DOT`, universal exact prices, or old eight-language copy in generated publishable sources/output. Matches in the handoff document are historical instructions and are not published.
- Local static HTTP crawl: all 101 HTML documents and required assets returned successfully; zero 404s or redirect loops.
- Static responsive/accessibility source checks at 320, 360, 375, 390, 414, 768, 1024, and 1440 CSS-pixel targets; logical properties, overflow guards, reserved image dimensions, focus styles, and reduced-motion CSS are present. RTL is emitted for `ar` and `fa`.
- `robots.txt` retains the sitemap declaration and explicit `OAI-SearchBot`, `Googlebot`, and `Bingbot` allow rules. `GPTBot` access was not changed.
- `manifest.json` contains only general international metadata. `CNAME` remains exactly `taro.mom`.
- Baseline has no `404.html`, privacy, terms, refund, or support documents; none were invented or linked.
- `openspec validate expand-site-to-20-locales --strict` passed.

## User-confirmed product facts

The product facts, supported languages, four Premium readings, credit packages, 50-credit activation/renewal wording, payment variants, Telegram constants, and disclaimer are based on the updated master description and the supplied localization handoff. They were not independently read back from the live bot.

## Not live-verified

The enabled bot catalog, current payment catalogs, prices, currency, payment availability, subscription terms, deck availability, referral behavior, PostgreSQL state, and n8n workflows were not live-verified. The site does not publish exact prices or internal payment values.

## Not yet native-reviewed

Native editorial review has not been completed for any of the 20 generated locale dictionaries. Technical schema and route checks pass, but grammar, idiom, terminology, RTL editorial quality, and market suitability still require qualified human review before deployment. This is a deployment blocker, not a claim of production readiness.

## Visual and deployment limitations

No browser executable or browser automation driver was available in the environment. The visual matrix is therefore source-level/static plus HTTP verification, not a claim of manual pixel review, browser zoom review, console review, or field Core Web Vitals. A deployment workflow was not run, and there is no production readback, indexing, ranking, CWV, or AI-citation evidence.

## Changed and generated files

Implementation sources:

- `sitegen/locales.json`
- `sitegen/routes.json`
- `sitegen/content/en.json`, `sitegen/content/ru.json`, and `sitegen/content/{id,ms,de,es,fr,it,nl,uz,pl,pt,tr,be,uk,kk,ar,fa,ko,hi}.json`
- `sitegen/templates/home.html`, `sitegen/templates/detail.html`
- `sitegen/assets/home.css`, `sitegen/assets/detail.css`
- `sitegen/implementation-notes.md`
- `tools/generate_site.py`, `tools/check_site.py`, `tools/test_sitegen.py`, `tools/http_smoke.py`, `tools/visual_smoke.py`, `tools/create_locale_content.py`

Generated/public outputs:

- `index.html`
- `en/index.html` legacy home redirect and four `/en/<detail>/index.html` pages
- 20 locale home `index.html` files and 80 canonical detail `index.html` files
- `en/reading.css`
- `sitemap.xml`
- `manifest.json`, `robots.txt`

OpenSpec artifact:

- `openspec/changes/expand-site-to-20-locales/verification-report.md`

Pre-existing user changes observed and preserved:

- `taro-bot-website-master-description.md`
- `taro-mom-localization-handoff-prompt.ru.md`

The reference images `images/referens.png` and `images/referens2.png` were inspected and not modified.

## Stop point

Tasks through 11.3 are local implementation/verification scope. No external deploy was performed. Tasks 11.4 and 12.x intentionally remain incomplete; archive and deployment require a separate explicit user decision after native review.

## 1. Зафиксировать baseline и границы

- [x] 1.1 Прочитать `AGENTS.md`, обновлённый `taro-bot-website-master-description.md`, все артефакты этого change и `taro-mom-localization-handoff-prompt.ru.md`; в implementation notes записать, что подтверждённый контракт равен 20 locales и 4 Premium readings.
- [x] 1.2 Записать текущие `git branch --show-current`, `git rev-parse HEAD` и `git status --short`; не изменять и не удалять handoff-файл пользователя и не перезаписывать несвязанные изменения.
- [x] 1.3 Создать baseline inventory всех public HTML files, canonical URL, redirect files, local assets, sitemap entries, `robots.txt`, `manifest.json` и `CNAME`; отдельно классифицировать 16 canonical pages и `/en/` redirect исходного состояния.
- [x] 1.4 Зафиксировать пять route keys: `home`, `daily-card`, `yes-no`, `three-card`, `relationships`; не добавлять detail types для Dawn или Premium readings.
- [x] 1.5 Поискать во всех source/public files hardcoded user strings, old eight-language claims/allowlists, две старые Premium entries, `Visconti`, `DOT`, Telegram URLs, exact prices и locale-specific route lists; сохранить команды и результаты как baseline в verification report.
- [x] 1.6 Проверить доступность live PostgreSQL/n8n read-only источника; если MCP отсутствует, явно записать «live bot catalog not verified; user-confirmed contract used» и не пытаться менять bot/n8n/PostgreSQL.

## 2. Создать каноническую модель локализации

- [x] 2.1 Создать `sitegen/locales.json` с ровно 20 locales в заданном порядке и полями `code`, `nativeLabel`, `englishName`, `dir`, `publicSegment`, `hreflang`, `ogLocale`, `homePath`; для `ar`/`fa` задать `rtl`, для `pt` сохранить segment `pt-br`, `hreflang=pt-BR` и `ogLocale=pt_BR`.
- [x] 2.2 Создать `sitegen/routes.json` с пятью route keys, English/Russian existing slug exceptions и default English detail slug для остальных locales; явно классифицировать `/en/` как noncanonical home redirect.
- [x] 2.3 Реализовать в `tools/generate_site.py` pure functions нормализации locale: lowercase base tag, `pt-BR` → `pt`, invalid/blank/`NULL`/disabled → `en`, diagnostic fallback requested → `en` → `ru`.
- [x] 2.4 Добавить unit-like self-tests для locale normalization, route construction и expected counts: 20 locales × 5 routes = 100 canonical pages плюс 1 redirect document.
- [x] 2.5 Создать English canonical schema в `sitegen/content/en.json`, включив common UI, home, четыре detail types, metadata, FAQ, disclaimer, alt/ARIA и structured content без HTML presentation.
- [x] 2.6 Создать полный `sitegen/content/ru.json` с тем же набором keys и типами; проверить совпадение placeholders и отсутствие blank/extra values.
- [x] 2.7 Реализовать schema validator в `tools/check_site.py`: exact keys/types, nonblank values, placeholder parity, inline-token allowlist, unique locale/route values и понятные сообщения `locale + route + key`.
- [x] 2.8 Добавить negative fixture/self-tests, доказывающие ненулевой exit при missing, blank, extra key, wrong type, mismatched placeholder и unknown locale; удалить временные fixtures после проверки либо хранить только безопасные test fixtures.

## 3. Создать шаблоны и детерминированный генератор

- [x] 3.1 Извлечь проверенную структуру текущего English home в `sitegen/templates/home.html`, сохранив landmarks, heading hierarchy, skip link, visible content без JavaScript и раннюю CTA.
- [x] 3.2 Объединить структуру четырёх current detail pages в `sitegen/templates/detail.html` с route-specific sections, breadcrumbs, related readings и locale-aware links.
- [x] 3.3 Вынести общие home styles в `sitegen/assets/home.css`, сохранив текущий дизайн; заменить direction-sensitive physical CSS properties на logical properties без визуального редизайна.
- [x] 3.4 Сохранить и при необходимости адаптировать `en/reading.css` как generated shared detail stylesheet; проверить root/nested paths и отсутствие зависимости от текущего directory depth.
- [x] 3.5 Реализовать HTML escaping, template substitution и deterministic ordering в `tools/generate_site.py`; запретить raw translated HTML, кроме явно документированного allowlist.
- [x] 3.6 Реализовать генерацию canonical, full 20-entry reciprocal `hreflang`, `x-default`, `lang`, `dir`, Open Graph/Twitter metadata и JSON-LD из тех же locale/route/content sources.
- [x] 3.7 Реализовать locale-aware language selector, breadcrumbs, reading-card и related-reading links, сохраняющие current route key.
- [x] 3.8 Реализовать генерацию `sitemap.xml` из canonical matrix; хранить truthful stable `lastmod`, который не меняется при no-op regeneration.
- [x] 3.9 Реализовать режимы `python tools/generate_site.py` и `python tools/generate_site.py --check`; `--check` не должен писать файлы и должен показывать missing/extra/changed output paths.
- [x] 3.10 Сгенерировать baseline `en`/`ru` pages и убедиться, что все существующие canonical paths и `/en/index.html` redirect сохранены до расширения на остальные locales.

## 4. Обновить подтверждённый продуктовый контент

- [x] 4.1 В English и Russian dictionaries заменить все claims про восемь языков на полный 20-language catalog во visible copy, FAQ, metadata, JSON-LD и selector.
- [x] 4.2 Добавить четыре Premium entries с точными card counts: Choice Between Two Options 7, Work & Finances 7, Celtic Cross 10, Year Ahead 12; использовать безопасные описания из master description.
- [x] 4.3 Обновить Premium/credits copy: packages 5/10/30, monthly Premium, 50 credits on activation и 50 after successful monthly renewal; не добавлять exact price.
- [x] 4.4 Реализовать два payment-copy variants: `ru` допускает YooKassa card/SBP и Telegram Stars; остальные 19 locales — Telegram Stars; current terms отдаются боту before purchase.
- [x] 4.5 Проверить полную product matrix: Daily Card, Yes/No, three-card, Dawn, five-card relationships, четыре Premium, additional card, contextual follow-up, history и profile fields.
- [x] 4.6 Добавить обязательный полный по смыслу disclaimer и safety copy для `en`/`ru`; убрать гарантии prediction/decision/mind-reading/partner return/income/financial success.
- [x] 4.7 Убедиться, что `Visconti`, публичный `DOT`, точные payment values/addresses/callbacks и неподтверждённые decks/features отсутствуют во всех publishable sources.
- [x] 4.8 Централизовать Telegram constants: conversion CTA точно `https://t.me/taroshenka_bot?start=ref974025936`, identity URL точно `https://t.me/taroshenka_bot`, username точно `@taroshenka_bot`.

## 5. Завершить восемь существующих локалей

- [x] 5.1 Создать/нормализовать полный `sitegen/content/de.json` с home и четырьмя detail pages; обновить 20-language и 4-Premium факты, metadata, FAQ, disclaimer, alt/ARIA.
- [x] 5.2 Создать/нормализовать полный `sitegen/content/es.json` с тем же coverage и проверками.
- [x] 5.3 Создать/нормализовать полный `sitegen/content/fr.json` с тем же coverage и проверками.
- [x] 5.4 Создать/нормализовать полный `sitegen/content/hi.json` с тем же coverage и проверками; сохранить естественную деванагари и `ltr`.
- [x] 5.5 Создать/нормализовать полный `sitegen/content/pt.json` на Portuguese (Brazil) с тем же coverage и проверками; не создавать отдельный `pt-BR` dictionary key.
- [x] 5.6 Создать/нормализовать полный `sitegen/content/tr.json` с тем же coverage и проверками.
- [x] 5.7 Для `en`, `ru`, `de`, `es`, `fr`, `hi`, `pt`, `tr` запустить schema/content checks и добиться missing=0, blank=0, extra=0 до перехода к новым locales.
- [x] 5.8 Сгенерировать 40 canonical pages первых восьми locales и проверить, что existing 16 canonical URLs не изменились, а добавлены ровно 24 недостающие detail pages.

## 6. Добавить 12 новых локалей — первая группа

- [x] 6.1 Создать полный `sitegen/content/id.json` на естественном Indonesian для home и четырёх detail routes; не оставлять English/Russian fragments вне allowlist.
- [x] 6.2 Создать полный `sitegen/content/ms.json` на естественном Malay с теми же требованиями.
- [x] 6.3 Создать полный `sitegen/content/it.json` на естественном Italian с теми же требованиями.
- [x] 6.4 Создать полный `sitegen/content/nl.json` на естественном Dutch с теми же требованиями.
- [x] 6.5 Создать полный `sitegen/content/uz.json` на естественном Uzbek с native label `Oʻzbek` и теми же требованиями.
- [x] 6.6 Создать полный `sitegen/content/pl.json` на естественном Polish с теми же требованиями.
- [x] 6.7 Запустить schema/content checks для `id`, `ms`, `it`, `nl`, `uz`, `pl`; исправить все missing/blank/extra/placeholder ошибки до генерации.
- [x] 6.8 Сгенерировать 30 canonical pages первой группы и HTTP-smoke-test их home/detail paths и assets.

## 7. Добавить 12 новых локалей — вторая группа и RTL

- [x] 7.1 Создать полный `sitegen/content/be.json` на естественном Belarusian с native label `Беларуская` и теми же требованиями.
- [x] 7.2 Создать полный `sitegen/content/uk.json` на естественном Ukrainian с native label `Українська` и теми же требованиями.
- [x] 7.3 Создать полный `sitegen/content/kk.json` на естественном Kazakh с native label `Қазақша` и теми же требованиями.
- [x] 7.4 Создать полный `sitegen/content/ar.json` на естественном Arabic; не использовать English/Russian fallback и обеспечить punctuation/content, пригодные для `rtl`.
- [x] 7.5 Создать полный `sitegen/content/fa.json` на естественном Persian; не использовать Arabic как подмену Persian и обеспечить `rtl`.
- [x] 7.6 Создать полный `sitegen/content/ko.json` на естественном Korean с native label `한국어` и теми же требованиями.
- [x] 7.7 Запустить schema/content checks для `be`, `uk`, `kk`, `ar`, `fa`, `ko`; исправить все missing/blank/extra/placeholder ошибки до генерации.
- [x] 7.8 Сгенерировать 30 canonical pages второй группы; проверить `lang`, `dir`, Unicode labels и HTTP paths.

## 8. Собрать полный SEO-граф и публичные fallback-файлы

- [x] 8.1 Сгенерировать все 100 canonical pages и подтвердить: 20 home + 80 detail; `/en/index.html` остаётся единственным noncanonical locale-home redirect.
- [x] 8.2 Проверить каждую страницу на self-canonical, 20 reciprocal hreflang entries и один route-equivalent `x-default`; исключить `/en/` home redirect из cluster, сохранив `/en/<detail>/` canonical pages.
- [x] 8.3 Перегенерировать `sitemap.xml` с ровно 100 `<loc>` и полными alternative sets; проверить равенство sitemap graph и HTML graph.
- [x] 8.4 Обновить `manifest.json` только общими международными metadata; не создавать ложную PWA-localization, если manifest не поддерживает locale-specific selection.
- [x] 8.5 Проверить `robots.txt`: sitemap declaration, crawlability, explicit `OAI-SearchBot` allow; не менять `GPTBot` access без нового user decision.
- [x] 8.6 Проверить, что `CNAME` всё ещё содержит только `taro.mom`, все public paths root-absolute/case-correct и нет server-only dependencies.
- [x] 8.7 Если в baseline отсутствуют `404.html`, privacy, terms, refund или support pages, не изобретать их; перечислить отсутствие в report и не добавлять ссылки на несуществующие документы.

## 9. Автоматическая приёмка

- [x] 9.1 Реализовать/report проверку ровно 20 locale codes, 5 route keys, 100 canonical pages, 101 total HTML documents с redirect и отсутствие competing allowlist.
- [x] 9.2 Для каждого locale сформировать строку отчёта: code, native label, direction, translation key count, route count=5, metadata coverage, missing count, blank count, link result; добиться missing=0 и blank=0.
- [x] 9.3 Parse-test каждый HTML document и JSON-LD block; проверить единственные `html`, `head`, `title`, canonical и h1, logical heading order и видимый FAQ/JSON-LD parity.
- [x] 9.4 Проверить каждую conversion CTA на exact referral URL и `rel` для new-tab links; проверить identity URL/username отдельно.
- [x] 9.5 Проверить четыре Premium readings, card counts, 20-language catalog, credits/payment variants, disclaimer semantic keys и полную product matrix во всех dictionaries/rendered homes.
- [x] 9.6 Запустить forbidden-content scan на eight-language claims/old allowlist, `Visconti`, public `DOT`, exact universal prices и prohibited guarantee patterns; вручную проверить потенциальные false positives.
- [x] 9.7 Crawl-test все internal links и local assets через локальный static HTTP server; добиться zero 404, redirect loops, orphan canonical pages и locale-dropping related links.
- [x] 9.8 Проверить изображения: existing files, exact case, real `src`, width/height, contextual localized `alt` либо empty decorative alt; не изменять `images/referens.png` и `images/referens2.png`.
- [x] 9.9 Запустить `python tools/generate_site.py --check`, `python tools/check_site.py` и `openspec validate expand-site-to-20-locales --strict`; сохранить exit codes/output в verification report.
- [x] 9.10 Запустить `git diff --check`, просмотреть `git diff --stat` и полный diff на secrets, temp profiles, screenshots, test artifacts, accidental `CNAME` change и unrelated edits.

## 10. Локальная визуальная и доступностная приёмка

- [x] 10.1 Поднять local static HTTP server из repository root; проверять HTTP routes, а не `file://`.
- [x] 10.2 Автоматически проверить horizontal overflow для всех 100 canonical routes хотя бы при 320 и 1440 CSS px; сохранить список routes и zero-failure result.
- [x] 10.3 Ручно проверить representative long-copy LTR locales на 320, 360, 375, 390, 414, 768, 1024 и 1440 px: menu, selector, headings, grids, FAQ, CTA и footer без clipping/overlap.
- [x] 10.4 Ручно проверить `ar` и `fa` home плюс все четыре detail types на mobile и desktop: reading order, logical alignment, menu, icons, cards, breadcrumbs, CTA и selector.
- [x] 10.5 Проверить 200% browser zoom/increased text, keyboard-only navigation, skip link, visible focus, touch target separation и `prefers-reduced-motion` на representative home/detail pages.
- [x] 10.6 Проверить работу без JavaScript: full important content, locale links, internal navigation, Telegram CTA и FAQ остаются доступными.
- [x] 10.7 Проверить отсутствие console/runtime errors и obvious spelling/encoding corruption; для каждого языка явно пометить native editorial review как passed либо deployment blocker.

## 11. Отчёт и обязательная остановка перед deploy

- [x] 11.1 Создать `openspec/changes/expand-site-to-20-locales/verification-report.md` с baseline commit/branch, commands, tool versions, generated counts, locale table, automated results, visual matrix, known limitations и точным списком changed/generated files.
- [x] 11.2 В отчёте явно разделить: locally verified, user-confirmed product facts, not live-verified bot/database facts, not yet native-reviewed translations и deployment-only checks.
- [x] 11.3 Убедиться, что все implementation/local-verification tasks 1–10 завершены, а внешний deploy не выполнялся; показать пользователю итоговый diff summary и запросить отдельное разрешение на deploy.
- [ ] 11.4 Не отмечать deployment tasks ниже выполненными, не архивировать change и не заявлять production/indexing/ranking/CWV/AI-citation результат до фактической публикации и readback.

## 12. Deployment-only — выполнять только после явного разрешения пользователя

- [ ] 12.1 Получить зафиксированное явное разрешение пользователя на внешний deploy конкретного проверенного commit/diff и подтверждение приемлемости remaining native-review blockers.
- [ ] 12.2 Выполнить разрешённый GitHub Pages deployment штатным проектным workflow без изменения `CNAME`; записать опубликованный commit/version и время.
- [ ] 12.3 Проверить production readback для всех 100 canonical URL, `/en/` redirect, representative assets, `robots.txt`, `sitemap.xml`, manifest, CTA, canonical/hreflang и отсутствие 404/loops.
- [ ] 12.4 После deploy рекомендовать/выполнить только с доступным ownership submit sitemap и inspect `/`, `/ru/`, `/en/` и representative new/RTL routes в Google Search Console и Bing Webmaster Tools; не фабриковать verification tokens или IndexNow key.
- [ ] 12.5 Обновить verification report production evidence, remaining risks и native review status; синхронизировать task checkboxes и архивировать change только после полной пользовательской приёмки.

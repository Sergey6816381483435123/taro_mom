# Основные правила taro.mom

## Mission

Build and maintain the 20-language website for the Tarot and Astro service at `https://taro.mom/`. Optimize first for useful, indexable, trustworthy content, then for clicks to the bot. Search rankings and AI citations are outcomes to improve toward, never guarantees to claim.

The implementation is a static site hosted on GitHub Pages. Keep the international English home page at `/`, the Russian home page at `/ru/`, and `en/index.html` only as the static legacy redirect from `/en/` to `/`. Do not introduce a framework, build system, backend, analytics, email capture, or another conversion path unless the user explicitly requests it.

## Sources of truth

Use these sources in this order:

1. `taro-bot-website-master-description.md` for product facts, allowed claims, tone, pricing language, features, languages, Premium details, and the disclaimer.
2. The fixed decisions and URLs in this file.
3. `index.html` for existing technical conventions and reusable site assets.
4. `images/referens.png` and `images/referens2.png` for visual direction only.

If sources conflict, preserve the higher-priority source and report the conflict. Never invent features, prices, testimonials, ratings, user counts, credentials, outcomes, contact details, or legal claims.

## Fixed decisions

- Publish the general English version at `/`; use `<html lang="en">`. Publish the Russian home page at `/ru/`; use `<html lang="ru">`.
- Preserve `/en/` only as a non-canonical legacy redirect to `https://taro.mom/`. Do not add `/en/` to sitemap, `hreflang`, visible language navigation, or JSON-LD as an independent page.
- Address a broad international English-speaking audience. Use clear, neutral international English. Create country-specific versions only when the user asks or when real regional differences in search demand, offer, payment, law, or terminology justify separate content.
- All-language revision `product-20261110`: show three conversion links in this order in every hero and final block:
  1. `https://t.me/taroshenka_bot?start=ref974025936`
  2. `https://t.me/astrology_1_bot?start=ref974025936` (chat, then launch Mini App button)
  3. `https://app.taro.mom/?ref=974025936`
- Browser referral requires the released Taro schema 105/backend r75 or a compatible successor. Preserve the first valid pending referral for up to 30 days and apply only on new-account registration. Do not conflate referral with source analytics.
- Preserve the entire `start=ref974025936` parameter. It is mandatory for referral attribution. Do not replace it with `https://t.me/taroshenka_bot`, a URL shortener, JavaScript redirect, or a different parameter.
- Use `@taroshenka_bot` and `https://t.me/taroshenka_bot` only for non-conversion identity references such as visible account naming or `sameAs`.
- The site URL and English canonical URL are both `https://taro.mom/`; the Russian canonical home URL is `https://taro.mom/ru/`.
- All one-page landing pages in this repository are published through GitHub Pages. Treat GitHub Pages compatibility as a release requirement.
- Do not add site email capture, forms, secondary offers or outbound conversion paths beyond the three approved entries. Support and identity links are informational.

## Работа с документацией

- Перед изменением контента, оформления, SEO или доступности прочитай `sitegen/PLAYBOOK.md`.
- Команды генерации, проверки и публикации описаны в `sitegen/README.md`.
- Сайт остаётся статическим и совместимым с GitHub Pages; сохраняй `CNAME`, регистр путей и работу без JavaScript. Не добавляй серверные зависимости без запроса.
- Не коммить секреты, временные профили браузера, QA screenshots и результаты тестов: репозиторий сайта публичный.

## All-language generation

Use tracked `python3 sitegen/generate.py` and `python3 sitegen/validate.py`. Registry and content cover 240 pages: 12 topics in each of 20 languages. Preserve existing paths, CNAME, `/en/` redirect and the shared legacy files protected by `sitegen/legacy-integrity.json`. Every topic has reciprocal 20-language alternates plus x-default; language links open the equivalent topic. Arabic/Persian use RTL. Brand: «Тарошенька» only in Russian, «Tarot» elsewhere; bot usernames stay unchanged. Screenshots use the real app with fictional fixtures and Rider–Waite cards. Do not run ignored legacy generators. See `sitegen/README.md`.

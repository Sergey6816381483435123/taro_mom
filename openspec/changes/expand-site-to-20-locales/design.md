## Context

На исходном commit `ae75039434661a01602de53483d33dbe48d13a81` ветки `main` сайт является статическим GitHub Pages-проектом без package manager и production build. Обнаружены 16 canonical HTML-страниц: восемь главных локалей и четыре пары английских/русских detail pages. Дополнительно `en/index.html` является неканоническим redirect главной `/en/` на `/`. Главные страницы представляют восемь почти самостоятельных копий большого HTML-документа; detail pages используют общий `en/reading.css`, но их текст и metadata также хранятся непосредственно в HTML.

Production-аудит от 13 августа 2026 года подтвердил видимые утверждения про восемь языков и только два Premium-расклада. Live-доступ к PostgreSQL/n8n из репозитория сайта отсутствует; пользователь явно подтвердил входной контракт handoff: 20 языков и четыре Premium-расклада. После этого `taro-bot-website-master-description.md` обновлён и снова является единым источником продуктовых фактов согласно `AGENTS.md`.

Изменение существенно шире незавершённого `localize-supported-languages`: тот change создал восьмиязычную базу и намеренно исключил полное покрытие detail pages. Новый change не переписывает его историю и использует текущее рабочее дерево как migration baseline.

## Goals / Non-Goals

**Goals:**

- Доставить ровно 20 главных страниц и все четыре существующих типа detail page на каждом языке: всего 100 canonical URL.
- Хранить каталог локалей, route matrix и translation keys в единственных машиночитаемых источниках.
- Генерировать полностью статический HTML, который работает на GitHub Pages и без JavaScript.
- Блокировать завершение при неполном переводе, неверной metadata, несогласованных ссылках, отсутствующем route или небезопасном продуктовом утверждении.
- Сохранить существующие URL, визуальную систему, контентную глубину и обязательную referral CTA.
- Обеспечить корректный RTL для арабского и персидского на mobile и desktop.
- Разделить локальную техническую готовность и разрешение на внешний deploy.

**Non-Goals:**

- Не создавать detail pages для Dawn или четырёх Premium-раскладов: таких типов страниц нет в baseline, а handoff запрещает создавать их механически.
- Не локализовать backend, Telegram-бот, n8n, PostgreSQL или платёжные каталоги и не проверять их состояние записью.
- Не добавлять аналитику, формы, email capture, backend, runtime locale detection, IP/geo redirect или другой conversion path.
- Не публиковать точные цены, DOT, Visconti, отзывы, рейтинги, гарантии результата или непроверенные юридические/контактные сведения.
- Не менять существующие индексируемые slug-и английских и русских detail pages и не выполнять внешний deploy.
- Не считать AI-перевод эквивалентом проверки носителем; языковая редактура остаётся deployment-only gate.

## Decisions

### 1. Два слоя: source content и сгенерированный статический сайт

Добавить `sitegen/` со следующими источниками:

- `sitegen/locales.json` — ровно 20 записей с `code`, `nativeLabel`, `englishName`, `dir`, `publicSegment`, `hreflang`, `ogLocale` и home URL;
- `sitegen/routes.json` — пять route keys (`home`, `daily-card`, `yes-no`, `three-card`, `relationships`), canonical path pattern и соответствия существующих English/Russian slug;
- `sitegen/content/<code>.json` — по одному полному словарю на locale с одинаковым набором ключей;
- `sitegen/templates/home.html` и `sitegen/templates/detail.html` — два семантических шаблона без локализованного prose;
- `sitegen/assets/home.css`, `sitegen/assets/detail.css` и минимальный общий JS только для существующих progressive-enhancement взаимодействий;
- `tools/generate_site.py` и `tools/check_site.py` на Python 3 standard library.

`generate_site.py` детерминированно создаёт и обновляет публичные HTML/CSS и `sitemap.xml`. Сгенерированные файлы коммитятся, поэтому GitHub Pages ничего не собирает. `check_site.py` сравнивает повторную генерацию с рабочим деревом и завершается с ненулевым кодом при drift.

Альтернативы: вручную поддерживать 100 HTML-файлов отклонено из-за неизбежного расхождения ключей и SEO-графа; framework/SSG с внешними пакетами отклонён как избыточный и несовместимый с минимальным production-стеком.

### 2. Каноническая locale matrix и нормализация

Порядок каталога фиксирован: `en`, `ru`, `id`, `ms`, `de`, `es`, `fr`, `it`, `nl`, `uz`, `pl`, `pt`, `tr`, `be`, `uk`, `kk`, `ar`, `fa`, `ko`, `hi`. Native labels берутся дословно из handoff. `ar` и `fa` имеют `dir=rtl`, остальные — `ltr`.

Locale key и `html lang` используют base code из каталога; исключение для публичной SEO-разметки португальской страницы: `hreflang=pt-BR`, `og:locale=pt_BR`, public segment `pt-br`, чтобы сохранить существующий бразильский URL и рыночную семантику. Входное значение `pt-BR` нормализуется в `pt`. Неизвестное, пустое или отключённое значение разрешается в `en`; content fallback для диагностического API генератора: requested → `en` → `ru`. Production generation при этом fail closed и не разрешает fallback заменять отсутствующий перевод.

Альтернатива — переименовать `/pt-br/` в `/pt/` — отклонена, поскольку текущий индексируемый URL существует и серверных 301 на GitHub Pages нет.

### 3. Стабильная матрица из 100 canonical routes

Главные URL сохраняются: English `/`, Russian `/ru/`, Portuguese `/pt-br/`, остальные `/<publicSegment>/`. `/en/index.html` остаётся только legacy redirect главной и не входит в canonical count.

Четыре английских detail URL сохраняются под `/en/`: `daily-tarot-card`, `yes-or-no-tarot`, `three-card-tarot-spread`, `love-tarot-reading`. Четыре русских существующих локализованных slug также сохраняются. Для остальных 18 локалей detail route строится как `/<publicSegment>/<english-detail-slug>/`. Английский slug в этом контексте является стабильным route identifier, а весь пользовательский контент, breadcrumbs и metadata локализуются. Это исключает неподдерживаемую миграцию URL и необходимость выдумывать 72 SEO-slug без языковой проверки.

Для каждого route key `x-default` указывает на английский эквивалент. Каждая canonical page содержит полный взаимный набор из 20 `hreflang` плюс `x-default`. `/en/` как главная не появляется в кластере, но `/en/<detail>/` остаются реальными canonical URL и альтернативами соответствующих detail pages.

### 4. Translation schema является строгим контрактом

English dictionary задаёт канонический набор ключей, но ни один locale-файл не может иметь missing, blank или extra keys. Значения должны быть строками или определёнными схемой списками/объектами; placeholders вида `{name}` и разрешённые inline tokens должны совпадать с English. HTML в переводах запрещён, кроме явно описанного небольшого allowlist, чтобы не смешивать content и presentation.

Каждый locale-файл содержит общие UI/metadata keys, полный home content, четыре detail page и route-specific SEO copy. Бренд `Taro.mom`, username `@taroshenka_bot`, CTA URL и технические route identifiers не переводятся. Генератор не подставляет русский или английский текст молча; fallback можно вызвать только отдельной диагностической проверкой, которая пишет warning и не используется для release output.

### 5. Контентная безопасность проверяется структурно и поиском

В каждом словаре обязательны: 20-language statement, четыре Premium reading entries, payment-safe copy, FAQ и полный по смыслу disclaimer. Валидатор проверяет наличие заданных semantic keys, а не только свободный поиск переведённых фраз. Дополнительно он сканирует исходники и output на старые fixed-eight allowlists, утверждения про восемь языков, `Visconti`, публичный `DOT`, точные цены и изменённые CTA.

Все conversion CTA должны буквально равняться `https://t.me/taroshenka_bot?start=ref974025936`; plain identity URL разрешён только в `sameAs` и видимом username. Payment copy различает `ru` (бот может показать YooKassa card/SBP и Telegram Stars) и остальные 19 локалей (Telegram Stars), не фиксируя цену.

### 6. Визуальная система сохраняется и становится direction-safe

Основные стили извлекаются из проверенной текущей страницы в общий generated asset без редизайна. CSS использует logical properties (`margin-inline`, `padding-inline`, `inset-inline`, `text-align:start`) там, где направление важно. Иконки направления и внешней ссылки не должны зеркалиться случайно. Меню, language selector, reading grids, CTA и breadcrumbs проверяются при `dir=rtl`.

Существующие оптимизированные изображения переиспользуются; новые изображения не нужны, поскольку изменение контентное и текущая графика не содержит локализуемого текста. Обе reference images остаются нетронутыми.

### 7. Проверки разделены на автоматические, ручные локальные и deployment-only

`python tools/generate_site.py --check` и `python tools/check_site.py` должны проверять schema, 100-route matrix, generated drift, HTML parsing, JSON-LD parsing, canonical/`hreflang`, internal links/assets, sitemap equality, CTA, lang/dir и запрещённые утверждения. Локальный static server используется для HTTP smoke test.

Ручная матрица включает ширины 320, 360, 375, 390, 414, 768, 1024 и 1440 px; на каждой достаточно проверить representative long-copy locales и обе RTL-локали, а автоматическая overflow probe проходит все routes. Browser zoom/increased text и keyboard focus проверяются отдельно.

Deployment-only gates: квалифицированная языковая проверка каждой локали, явное разрешение пользователя, production readback, Search Console/Bing submission. Отсутствие live bot/database access и native review отмечается честно и не маскируется успешными техническими тестами.

## Risks / Trade-offs

- [AI-перевод может быть грамматически корректным, но неестественным] → хранить locale review report, запрещать внешний deploy до квалифицированной проверки всех 20 языков.
- [100 страниц и полный `hreflang` увеличат HTML и sitemap] → генерировать единообразно, проверять reciprocal graph и не добавлять несуществующие типы страниц.
- [Генератор создаёт новый локальный workflow] → использовать только Python standard library, коммитить output и проверять drift; production остаётся обычным static site.
- [English slug в неанглийских detail URL слабее локального SEO-slug] → предпочесть стабильность и отсутствие redirect migration; рассматривать локализованные slug отдельным change после исследования и возможности 301.
- [RTL может выявить предположения текущего CSS] → logical properties, отдельная автоматическая проверка `dir` и ручная проверка `ar`/`fa` на mobile/desktop.
- [Старый незавершённый change создаёт путаницу] → новый change является единственной задачей для 20-язычного расширения; не отмечать и не переписывать checkbox старого change.
- [Сгенерированные source JSON доступны как обычные GitHub Pages assets] → не хранить в них секреты или внутренние bot/payment данные; всё в репозитории считать публичным.

## Migration Plan

1. Зафиксировать baseline inventory и сохранить все существующие canonical paths.
2. Создать manifests, templates, dictionaries и validators, затем воспроизвести существующие страницы без изменения URL.
3. Обновить восемь существующих локалей до новой продуктовой матрицы и добавить их недостающие detail pages.
4. Добавить 12 новых полных словарей и сгенерировать их 60 страниц.
5. Перегенерировать sitemap и весь SEO-граф; сохранить `en/index.html`, `robots.txt` и `CNAME` согласно контракту.
6. Выполнить автоматические и ручные локальные проверки, сформировать locale coverage report и остановиться перед deploy.
7. После отдельного разрешения опубликовать, проверить production readback и только затем завершить deployment tasks.

Откат до deploy выполняется возвратом change diff. После deploy откат выполняется публикацией предыдущего известного исправного commit; существующие canonical URL не меняются, поэтому redirect rollback не требуется.

## Open Questions

Открытых решений, блокирующих локальную реализацию, нет. Live-проверка enabled-каталога бота и проверка переводов носителями недоступны в текущем окружении; каталог и продуктовые факты подтверждены пользователем, а языковая проверка явно отнесена к deployment gate.

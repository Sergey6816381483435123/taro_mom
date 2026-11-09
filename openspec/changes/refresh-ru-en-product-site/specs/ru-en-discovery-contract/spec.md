## ADDED Requirements

### Requirement: Маршруты совместимы с GitHub Pages
Все routes SHALL обслуживаться реальными статическими файлами с case-sensitive root-absolute asset paths. `/` SHALL быть EN self-canonical, `/ru/` — RU self-canonical; `CNAME` SHALL сохранять `taro.mom`. `/en/` SHALL оставаться минимальным static legacy redirect на `/`. Его redirect MUST NOT охватывать `/en/<topic>/`. MUST NOT вводить SSR, backend сайта, custom headers/rewrites либо runtime environment dependencies.

#### Scenario: Проверка legacy route и его дочерней темы
- **GIVEN** plain static HTTP server запущен из корня опубликованного набора
- **WHEN** запрашиваются `/en/` и `/en/daily-tarot-card/`
- **THEN** первый документ имеет redirect signals на `/` и видимую ссылку, а второй остаётся самостоятельной canonical detail page с рабочими assets

### Requirement: Language graph связывает только эквиваленты
Home и existing Tarot detail SHALL сохранять действующие canonical URL и reciprocal language clusters. Новые Astro topics SHALL иметь только EN/RU эквиваленты и x-default на EN той же темы. Self-canonical и абсолютные hreflang SHALL быть взаимными. MUST NOT включать `/en/` redirect, несуществующие переводы или locale homes как эквивалент Astro detail. Переключение языка SHALL быть ручным.

#### Scenario: Astro detail доступен только на двух языках
- **GIVEN** существует пара transit pages RU/EN, другие переводы ещё не делались
- **WHEN** проверяются head, sitemap и language navigation
- **THEN** topic alternates содержат только RU/EN/x-default; ссылки на другие языковые главные отдельно подписаны и не являются hreflang темы

### Requirement: Метаданные и JSON-LD отражают видимое содержание
Каждая из 24 страниц SHALL иметь уникальные локализованные title/description/OG/Twitter, canonical и representative social image. Connected graph SHALL использовать стабильные WebSite/WebPage/SoftwareApplication IDs; идентичность приложения едина. PotentialAction SHALL отражать три проверенных назначения в общем порядке. JSON-LD MUST парситься и совпадать с текстом; MUST NOT содержать неподтверждённые Review/AggregateRating, цены, авторство, organization claims. FAQPage, если сохраняется, SHALL совпадать с видимым FAQ и MUST NOT объявляться гарантией rich result.

#### Scenario: Проверка новой Moon page
- **GIVEN** видимая страница описывает календарь и дневник
- **WHEN** validator читает metadata/graph
- **THEN** разметка описывает эту страницу, не добавляет медицинские обещания/ratings и содержит те же корректные action targets, что HTML

### Requirement: Crawl policy и sitemap поддерживают обнаружение
`robots.txt` SHALL сохранять sitemap declaration и доступ к публичным страницам/критическим assets для Googlebot, Bingbot и OAI-SearchBot. GPTBot training policy MUST NOT меняться без отдельного решения. Sitemap SHALL сохранять existing canonical URLs и добавить 14 новых Astro URLs; lastmod SHALL отражать реальное изменение, не переписывая даты других локалей. MUST NOT вводить bot challenge, forced locale redirect, `meta keywords`, hidden AI-only content или `llms.txt` вместо обычной доступности.

#### Scenario: Генератор выполняется без изменений контента
- **GIVEN** дата запуска новая, но existing non-RU/EN страницы не изменялись
- **WHEN** пересоздаётся sitemap
- **THEN** их lastmod и canonical URL сохраняются, а `/en/` redirect не добавляется в индексируемый набор

### Requirement: Генерация воспроизводима и ограничена RU/EN
Необходимые offline generator/validators SHALL быть доступны в tracked публично безопасных файлах. Generation SHALL явно учитывать locale/route coverage и content revision; новые Astro routes MUST NOT автоматически размножаться на 18 неподготовленных локалей. Existing non-RU/EN HTML и их rendered styling SHALL сохраняться; изменение общего ресурса SHALL требовать проверки всех его потребителей. Assets/CNAME и сопоставление source→HTML SHALL проверяться перед выпуском.

#### Scenario: Общий генератор получил новую Astro route
- **GIVEN** Astro content существует только для RU/EN
- **WHEN** выполняется сборка статического набора
- **THEN** создаются ровно 14 новых Astro pages, отсутствует fallback на чужой язык, а existing other-locale pages не получают новый layout/CTA от общего шаблона

### Requirement: SEO/GEO оценивается без выдуманных результатов
Контент SHALL давать самостоятельные видимые ответы, определения, исходные данные, примеры и ограничения для реальных функций. Проверки SHALL разделять local static/browser, опубликованный HTTP/Telegram flow и внешние результаты поиска. Индексация, позиции, field CWV и AI citations MUST NOT считаться достигнутыми по OpenSpec validation, crawler allow rule, JSON-LD либо лабораторному тесту. Требования SHALL опираться на `reference/search-guidance.md` и обновляться при изменении первичной документации.

#### Scenario: Все локальные проверки прошли
- **GIVEN** страницы работают через локальный static server
- **WHEN** оформляется отчёт готовности
- **THEN** local evidence перечислено отдельно; indexing, Search Console/Bing inspection, live referrals и field metrics помечены только по реальным внешним результатам либо как непроверенные

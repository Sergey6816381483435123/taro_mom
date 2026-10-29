## ADDED Requirements

### Requirement: Существующие canonical URL сохраняются
Root `/` SHALL оставаться English home и `x-default`; `/ru/` SHALL оставаться Russian home; `/pt-br/` SHALL оставаться Brazilian Portuguese home. `/en/` SHALL оставаться только статическим legacy redirect home на `/`, отсутствовать в sitemap и language cluster. Существующие English detail routes под `/en/` и Russian localized detail routes SHALL сохраняться как canonical URL.

#### Scenario: Отличие English home от English details
- **GIVEN** проверяются маршруты `/en/` и `/en/daily-tarot-card/`
- **WHEN** валидатор классифицирует их
- **THEN** `/en/` является неканоническим redirect на `/`, а `/en/daily-tarot-card/` является canonical English detail page

### Requirement: Новые detail routes имеют стабильную схему
Для locales кроме English и Russian каждый detail route SHALL использовать `/<publicSegment>/<english-detail-slug>/`; весь видимый текст и metadata SHALL оставаться локализованным. Реализация MUST NOT переименовывать существующие indexable slug или создавать redirect plan, недоступный на GitHub Pages.

#### Scenario: Построение корейского route
- **GIVEN** route key `daily-card` и locale `ko`
- **WHEN** generator строит canonical path
- **THEN** path равен `/ko/daily-tarot-card/`, а документ имеет Korean content и `lang="ko"`

### Requirement: Каждая canonical page имеет полный reciprocal hreflang cluster
Каждая из 100 страниц SHALL иметь self-canonical, 20 взаимных `hreflang` equivalents текущего route key и один `x-default` на English equivalent. `hreflang` SHALL использовать canonical base codes, кроме подтверждённого `pt-BR`; каждый target SHALL быть существующим canonical URL, который ссылается обратно.

#### Scenario: Отсутствует обратная альтернатива
- **GIVEN** одна page ссылается на locale equivalent, который не ссылается обратно
- **WHEN** выполняется graph validation
- **THEN** release check завершается ошибкой с обеими URL и missing hreflang

### Requirement: Sitemap точно отражает canonical graph
`sitemap.xml` SHALL содержать все и только 100 canonical URL и их полные alternative sets. `/en/` redirect MUST NOT присутствовать. `lastmod` SHALL отражать реальную дату существенного изменения output и MUST NOT обновляться только из-за повторного запуска генератора.

#### Scenario: Сравнение sitemap и HTML
- **GIVEN** сайт сгенерирован
- **WHEN** validator сравнивает sitemap loc/alternates с HTML canonical/alternates
- **THEN** множества полностью совпадают и каждый path соответствует существующему case-sensitive file

### Requirement: Metadata и JSON-LD локализованы и согласованы
Каждая canonical page SHALL иметь unique localized `title`, meta description, Open Graph/Twitter metadata и valid JSON-LD, соответствующие видимому контенту. Home SHALL использовать связанный `WebSite`, `WebPage`, `SoftwareApplication` и видимый `FAQPage`; detail pages SHALL размечать только видимые сущности. `potentialAction.target` SHALL использовать обязательную referral CTA, а `sameAs` SHALL использовать plain identity URL.

#### Scenario: JSON-LD расходится с видимым FAQ
- **GIVEN** FAQ answer в JSON-LD не совпадает по смыслу с rendered answer
- **WHEN** structured-data check сравнивает значения из одного translation source
- **THEN** generation или validation завершается ошибкой

### Requirement: Внутренние ссылки сохраняют locale и не создают orphan pages
Navigation, reading cards, breadcrumbs, related-reading links и footer links SHALL вести на canonical эквиваленты текущей locale, кроме явной language switch и Telegram identity/CTA. Каждый canonical route SHALL быть достижим из locale home или related navigation и MUST NOT возвращать 404.

#### Scenario: Проверка внутренних ссылок
- **GIVEN** generated site обслуживается локальным static HTTP server
- **WHEN** crawler проходит все internal href и asset paths
- **THEN** каждый target успешен, не создаёт loop и не теряет locale без явного намерения

### Requirement: Crawl controls сохраняют GitHub Pages discovery
`robots.txt` SHALL разрешать crawl canonical pages и render-critical assets, сохранять sitemap declaration и явный allow для `OAI-SearchBot`. Настройка `GPTBot` MUST NOT изменяться без отдельного решения. `CNAME` SHALL оставаться `taro.mom`.

#### Scenario: Предрелизная инфраструктурная проверка
- **GIVEN** route и asset changes завершены
- **WHEN** проверяются `CNAME`, `robots.txt`, `sitemap.xml` и legacy redirect вместе
- **THEN** custom domain сохранён, canonical content crawlable, sitemap объявлен, а redirect не включён как canonical

## Context

Решения владельца от 9 ноября 2026 года зафиксированы в proposal. Сайт — отдельный GitHub Pages repo; приложение — Go/React в `/opt/stacks/bots/Taro`, публичный origin `https://app.taro.mom/`. Перенос сайта в приложение не требуется.

Нынешние страницы генерируются из `sitegen/`, но используемые scripts в `tools/` игнорируются Git. Общие templates/CSS обслуживают 20 локалей. Архивный контракт требует ровно четыре Premium-расклада и единственный CTA; он больше не соответствует согласованному обновлению RU/EN. Факты и ограничения: [реестр](reference/fact-register.md). Полный список 24 страниц и briefs: [план](reference/page-plan.md).

## Goals / Non-Goals

**Goals:** достоверное описание Таро/Астро; все 10 existing RU/EN pages и 14 новых Astro pages; сохранённый брендовый стиль с настоящим UI; три входа с доказанной referral attribution; полезный индексируемый HTML; воспроизводимая статическая публикация без влияния на другие языки.

**Non-Goals:** реализация или публикация в этапе подготовки; переводы на другие 18 языков; новые страницы Таро сверх текущих четырёх на язык; backend сайта, аналитика, формы, email capture, цены в валюте, redesign приложения, новые боты/БД, новые функции Таро/Астро. Приложение может получить отдельное изменение для атрибуции при последующей реализации; этот документ не разрешает production-записи.

## Decisions

### 1. Отдельная продуктовая редакция с реестром доказательств

`reference/product-description.md` — draft новой опоры, а не объявление всех features доступными в production. При реализации сначала сверить рабочий каталог и перенести подтверждённый текст в корневой `taro-bot-website-master-description.md`, затем согласовать AGENTS/OpenSpec context/текущие validators с решениями владельца. Старый архив сохраняется. Не строить новый контент на прежнем правиле «ровно четыре Premium».

Для каждого изменяемого claim хранить источник/дату/уровень проверки. Механика из исходников допустима для проектирования; enabled/price/Premium/pack/bonus/language count требует сверки перед публикацией. Сайт использует общую формулировку о кредитах и Premium, без точных цен и неподтверждённых размеров бонусов. Наличие Premium не подразумевает безлимитность.

Альтернатива — заменить несколько абзацев на основе старого master — сохраняет неправильную модель продукта и отклонена.

### 2. Архитектура страниц и сохранение URL

Сохранить `/`, `/ru/` и восемь существующих detail URL. `/en/` остаётся статическим redirect, но его `/en/<topic>/` дочерние страницы остаются canonical. Добавить Astro overview и шесть тем на язык строго по матрице. Hub и detail отвечают на разные вопросы; дневник описывается на Moon page, личные события — на transit page, краткий натальный портрет — на natal page. Это исключает отдельные малосодержательные страницы.

Таро приоритетно в hero, navigation и главном каталоге. В Астро-detail контент посвящён теме Астро, а три входа сохраняют общий порядок. Новые country/date/sign/city варианты не создавать.

### 3. Единый контракт трёх входов

| Порядок | Назначение | Контракт URL | Состояние |
|---|---|---|---|
| 1 | Тарошенька, Telegram chat | `https://t.me/taroshenka_bot?start=ref974025936` | Действующий точный адрес. Не оборачивать в `/go`, не добавлять параметры. |
| 2 | Астро Mini App через Telegram | `https://t.me/astrology_1_bot?start=ref974025936` | Статически подтверждён Astro `/start` referral path, затем кнопка запуска приложения; live launch — выпускная проверка. |
| 3 | Браузер | `https://app.taro.mom/?ref=974025936` | Целевой новый контракт. Сейчас не доказана обработка `ref`; не публиковать до реализации/проверки. |

Astro chat entry использует общий normalizer и `webapp/postgres/entry.go:47`: ReferrerID передаётся в RegisterWeb при новом профиле. Поэтому baseline второго входа двухшаговый и сохраняет referral до открытия приложения. Подпись объясняет запуск Mini App кнопкой; не обещать немедленного открытия поверх Telegram.

Прямой `?startapp=ref974025936` — только возможное улучшение после проверки Main Mini App и доработки создания referral из подписанного `start_param`. Он не нужен baseline и не заменяет проверку referral lifecycle. Скрыто переводить второй вход в Тарошеньку или третий в Telegram нельзя.

Полный блок входов — в hero и конце каждой страницы, источник порядка един. Первый визуально основной; второй и третий видимы, доступны клавиатурой, без dropdown/JS. Одиночные компактные CTA ведут только в первый вход, не подменяя блок. `target=_blank` требует `rel="noopener noreferrer"`. Identity links и sameAs могут быть без referral.

### 4. Атрибуция в приложении — отдельная зависимость

Referrer `974025936` — пользовательская связь приглашения. Source/campaign — отдельный необязательный маркетинговый атрибут. Сайт не получает новый analytics script/backend. Существующий `/go/<code>` ведёт на `m_...` и сам не выполняет договорённость о referral; он не применяется вместо этих CTA.

Для browser entry в отдельном Taro change:

- `ref` публичен и не является доказательством identity. Сервер валидирует синтаксис, существование inviter и отсутствие self-referral. Допустимы только штатные same-origin endpoints, без произвольного redirect target.
- Первый валидный ref сохраняется как pending на 30 дней. Повторный переход в этом окне не меняет первый ref; после срока новый valid ref может создать новый pending. Некорректный ref не блокирует вход и не стирает valid pending.
- Pending хранится first-party сервером, browser получает ограниченный непрозрачный cookie (`Secure`, `HttpOnly`, `SameSite=Lax`, `Path=/`; без Domain для `__Host-` варианта). Не хранить identity/вопросы/email в CTA или marketing identifiers. Цель хранения объясняется в действующей информации о данных приложения; для сайта отдельный сбор данных не добавляется.
- Pending переживает Telegram OAuth round trip и email-first verification/password creation. Для email verification на другом устройстве связь хранится в регистрационном intent на сервере и ограничивается более коротким из сроков intent/referral. Не менять одноразовый email token и не добавлять сырой ref к внешним redirect URL.
- Referral relationship создаётся атомарно только с новым canonical account и валидным пригласившим. Наличие ранее созданного аккаунта исключает ретроактивное присвоение inviter, включая аккаунт без inviter.
- Пользователь с активной сессией сохраняет свою identity и существующую referral relationship; новый ref не меняет их. Linking/merge требует proof обеих identities и явного подтверждения. Допустимый штатный merge сохраняет финансовую/referral history без повторной награды. Если histories несовместимы и текущий contract не обеспечивает безопасного объединения, merge явно отклоняется с сохранением аккаунтов; новый механизм произвольного выбора inviter не вводится.
- First-touch referral и first/last marketing touch хранятся раздельно. В этом change не создаются новые кампании и не вводятся дополнительные UTM-обязательства.
- Reward не выдаётся за клик/логин/повтор открытия. Существующий доменный eligible event (первый сохранённый основной расклад) должен завершать ту же referral lifecycle в допустимых каналах с идемпотентностью. Виды Astro-операций не расширяют основание выплаты автоматически. Поведение existing аккаунта при входе без новой связи считается корректным сохранением атрибуции.

Альтернатива — query parameter без сохранения/проверки или click counter — отклонена: она не доказывает signup-to-referral и может теряться при входе/письме. Дополнение обязанностей Taro фиксируется здесь контрактом, без SQL/API implementation в repo сайта.

### 5. RU/EN и 18 сохранённых локалей

Добавить явное различение revision/route coverage при generation: RU/EN получают новый контент, новые routes и обновлённые page types; остальные 18 словарей/страниц/публичных CSS-контрактов не пересобираются без необходимости. Новые Astro routes имеют coverage только `ru,en`.

Шаблоны/CSS новой revision применяются по manifest к RU/EN. Допустимо сохранить старые шаблоны/CSS для иных локалей; не дублировать вручную весь опубликованный HTML. Если общий ресурс меняется, требуются regression render/asset checks всех его потребителей. Выбранное правило: existing non-RU/EN HTML и их rendered styling остаются неизменными; sitemap — общий и расширяется.

Нужные offline generator/validators перевести из игнорируемого `tools/` в проверяемый tracked `sitegen/` location либо узко allowlist конкретные файлы. Выбрать первый вариант, предварительно проверив imports/dependencies. Не отслеживать весь `tools/`, browser profiles, QA artifacts или secrets. Статический сайт не требует выполнения Python/JS на GitHub Pages; готовые HTML/assets публикуются как прежде.

### 6. SEO/GEO и язык темы

Каждая страница self-canonical; head содержит абсолютные и взаимные hreflang на эквиваленты. Home/existing Tarot clusters сохраняют существующие 20 локалей, поскольку их URL не меняются и темы остаются эквивалентными; свежесть перевода не выдумывать. Новые Astro clusters имеют только RU, EN и x-default на EN той же темы. Нельзя подставлять другие locale homes как Astro equivalents.

Language nav на новой Astro page предлагает RU/EN эквиваленты; отдельно обозначенный переход к другим языковым главным разрешён. `/en/` не входит в sitemap/alternates/JSON-LD; `/en/<topic>/` входит по-прежнему. Existing sitemap lastmod иных языков не менять; updated/new RU/EN — дата реального изменения контента, не дата каждого запуска генератора.

Использовать компактный graph WebSite/WebPage/SoftwareApplication со стабильными IDs (`https://taro.mom/#website`, `#application`, `<canonical>#webpage`). Public software identity едина; две bot identities допустимы только как подтверждённые sameAs; нельзя выдумывать publisher credentials/reviews/offers. WebPage potentialAction перечисляет три подтверждённых target в том же порядке; action targets не меняют canonical. FAQ видим пользователю; FAQPage не требуется. Если сохраняется — разметить только действительные вопросы и ответы, не обещать rich result.

GEO здесь означает понятные извлекаемые ответы о реальном продукте: определения, исходные данные, результат, условия, примеры и ограничения. Никаких гарантий цитирования, hidden AI text, специальных schema для AI, `meta keywords`, `llms.txt` или искусственных страниц. Источники и проверки — [search guidance](reference/search-guidance.md).

### 7. Визуальная система и assets

Сохранить осмотренные reference palette/иллюстрации и Cormorant Garamond/Inter. Нужны лёгкие тёмные панели, читаемые CTA, реальные UI examples с отдельным текстом. Production examples используют демонстрационные данные и проходят проверку приватности; QA screenshots не публикуются. Новые AI-картинки генерируются только если подтверждена потребность, с обоими reference и последующей оптимизацией.

HTML-текст, semantic landmarks, один h1, heading hierarchy, skip link, focus и keyboard не зависят от JS. От 320 px — одна колонка, без fixed height текста и горизонтальной прокрутки. Контраст уровня WCAG 2.2 AA, reduced motion, alt, width/height обязательны. Проверить 320/360/375/390/414/768/1024/1440 px, portrait/landscape, 200% zoom и increased text. Hero оптимизирован, ниже fold lazy loading. Лабораторные CWV не называть полевыми значениями; LCP/INP/CLS цели из playbook сохраняются.

## Risks / Trade-offs

- [Browser ref ещё не реализован] → отдельная Taro dependency и обязательное сквозное доказательство до публикации трёх входов.
- [Main Mini App не проверен] → baseline через Astro `/start ref...` и видимую инструкцию кнопки; прямой launch только после acceptance.
- [Сложный dynamic access] → текущий quote/use-case важнее старого README/каталога; no exact currency/bonus claims; live read-only сверка.
- [Факты отличаются между каналами] → channel matrix; не обещать, что все функции доступны в каждом интерфейсе. Existing card-of-day route требует отдельной сверки.
- [Общий template/CSS меняет переводы] → revision-scoped rendering, hash/inventory и visual regression для фактически общих ресурсов.
- [Новые pages остаются orphan] → обзор/навигация/related links и crawl graph от обеих главных.
- [Marketing конфликтует с referral] → раздельные данные; неизменная первая CTA; тест bonus lifecycle, не только click.
- [Непроверенные legal/support URLs] → использовать только подтверждённые документы/поддержку; не добавлять фиктивные реквизиты. Если необходимый документ отсутствует, явно оставить проверку выпуска невыполненной.

## Migration Plan

1. Сверить рабочие факты/entry configuration и подготовить отдельное изменение Taro для browser attribution. Переносить только подтверждённые claims в master.
2. Согласовать текущие проектные правила/validators с тремя входами и обновлённым каталогом; восстановить tracked generation и RU/EN coverage.
3. Реализовать 24 страницы/assets/metadata. Регенерировать только явно выбранные routes; проверять baseline иных языков и CNAME.
4. Выполнить local static HTTP crawl, metadata/JSON-LD/referral checks и required visual/accessibility matrix. Согласованный объём не сокращается при сбое зависимости.
5. После готовности Taro dependency выполнить E2E трёх входов на разрешённых тестовых identities: new/existing, OAuth/email, retries/linking/expiry. Не делать покупки и не выдавать ручные бонусы для имитации успеха.
6. Подготовить reviewable site commit/diff и запросить отдельное разрешение на публикацию. После разрешения — GitHub Pages из этого repo, проверка 24 URL и `/en/` redirect, HTTPS/assets/crawl/referrals. Отправка sitemap/проверка Search Console/Bing — отдельные внешние действия при наличии доступа/разрешения.
7. Откат сайта — возврат выделенного site commit с прежними страницами/assets/sitemap. Откат browser attribution в Taro самостоятельный и должен сохранять уже созданные referral relationships, финансовую историю и existing identities. Удаление новых страниц только до их публикации либо отдельным решением по redirect; не удалять уже индексируемые URL ради простого отката CSS.

## Open Questions

Дополнительных продуктовых вопросов владельцу нет: решения приняты. Неизвестные относятся к проверкам реализации: текущая конфигурация Telegram launch, enabled catalogue/access, legal/support destinations, live browser/signup attribution. Они имеют ответственного и критерии в tasks; их не подменять предположением или статусом «проверено».

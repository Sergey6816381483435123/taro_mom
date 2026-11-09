## 1. Актуальные факты и согласование источников

- [x] 1.1 Проверить read-only текущие публичные входы, enabled RU/EN catalogue, channel coverage и dynamic access; обновить `reference/fact-register.md` датами/доказательствами, включая карту дня, справку карт и различия Astro replay.
- [x] 1.2 Проверить реальные legal/support destinations, способы оплаты, языки и изменяемые бонусы; оставить в публичном тексте только подтверждённые необходимые сведения без точных денежных цен.
- [x] 1.3 На основе подтверждённой редакции `reference/product-description.md` обновить корневой master и согласовать текущие AGENTS/OpenSpec context/validators с тремя входами и новым каталогом. Не менять архивные документы и старое активное change.

## 2. Внешняя зависимость Taro: атрибуция трёх входов

Ответственный repo: `/opt/stacks/bots/Taro`. Отдельное изменение: `add-browser-referral-attribution`. Пользователь разрешил реализацию и публикацию после подготовки спецификаций. Пункты 2.1–2.4 обязательны до выпуска сайта. Дизайн/контракт: `design.md`, разделы 3–4, `specs/three-entry-attribution/spec.md`.

- [x] 2.1 Подтвердить штатный main `/start ref...` и Astro `/start ref...` → кнопка Mini App, один canonical account и неизменность inviter existing users. Сохранить двухшаговый baseline; direct startapp не вводить без отдельного доказательства launch/referral lifecycle.
- [x] 2.2 В отдельном Taro change реализовать browser `?ref=974025936`: валидацию, серверный first-valid pending на 30 дней и передачу через OAuth/email intent, включая подтверждение на другом устройстве; проверить cookie/expiry/invalid/self-referral и отсутствие account effect от одного клика.
- [x] 2.3 Проверить атомарность/idempotency referral creation, существующий eligible reward event в трёх каналах, retry/concurrency и linking/merge invariants без перепривязки existing inviter или повторной награды. Сохранить отдельность source/campaign tracking.
- [x] 2.4 Зафиксировать проверенный URL registry и результаты безопасных integration/E2E для new/existing identities; реальные launch/API и финансовые fixtures/rollback отразить раздельно. Если dependency не готова, оставить публикацию RU/EN невыполненной, сохранив весь согласованный объём.

## 3. Воспроизводимая статика и ограничения локалей

Зависит от 1.3; черновой layout может готовиться параллельно секции 2.

- [x] 3.1 Сделать необходимые generator/validators tracked и воспроизводимыми из чистого checkout, адресно перенеся проверенные scripts из игнорируемого `tools/`; исключить credentials, QA output и временные зависимости. Документировать команды.
- [x] 3.2 Ввести явные revision/coverage rules для 24 RU/EN routes из page plan и сохранённой версии других локалей; проверить, что Astro не размножается на все 20 языков.
- [x] 3.3 Зафиксировать baseline inventory/hash existing иных локалей и используемых ими assets, CNAME, legacy redirect и sitemap. Подготовить scope check, ловящий побочные изменения общих templates/CSS.

## 4. Содержание и страницы RU/EN

Зависит от 1 и 3; CTA registry финализируется после 2. Все пункты включают естественную редактуру обоих языков, metadata, FAQ и disclaimer, а не только HTML-каркас.

- [x] 4.1 Обновить обе home: Таро первым, актуальные сценарии/AI/история/справка, Astro preview, аккаунт/кредиты/Premium и три входа.
- [x] 4.2 Обновить пары страниц «Карта дня» и «Да/нет» с прежними URL, достоверными сценариями и рабочими related/language links.
- [x] 4.3 Обновить пары «Три карты» и «Отношения», включая границы интерпретации чувств/исходов и контекст актуальных дополнительных сценариев.
- [x] 4.4 Создать Astro overview RU/EN и навигацию по шести темам с объяснением направлений/интерфейсов и необходимых данных.
- [x] 4.5 Создать пары Astro natal chart и compatibility: самостоятельные ответы, различия форматов, input requirements и примеры.
- [x] 4.6 Создать пары Astro horoscopes и transits, включая личные события без неподтверждённых горизонтов/цен/trial promises.
- [x] 4.7 Создать пары Astro solar return и Moon calendar/journal, без гарантий будущего и медицинских claims.

## 5. Общий интерфейс, assets и техническое обнаружение

Зависит от 3; применяется ко всем страницам секции 4.

- [x] 5.1 Реализовать mobile-first template revision и единый entry block в hero/конце каждой страницы; сохранить DOM/визуальный порядок, touch/focus и видимость трёх ссылок без JS.
- [x] 5.2 Подготовить curated product images реального UI с демонстрационными данными RU/EN, оптимизацией, dimensions/fallback/alt; переиспользовать existing artwork, новые иллюстрации создавать только при доказанной нужде.
- [x] 5.3 Согласовать canonical/hreflang и language navigation: existing clusters сохраняются, Astro только RU/EN/x-default той же темы; проверить `/en/` отдельно от `/en/<topic>/`.
- [x] 5.4 Обновить connected JSON-LD, social metadata и manifest/branding где требуется; action targets соответствуют трём проверенным CTA. Обновить sitemap только для фактически изменённых/новых страниц, сохранить robots/GPTBot policy/CNAME.

## 6. Локальная проверка без публикации

Зависит от 2–5 для финальной готовности. Проверки до готовности dependency допустимы, но не закрывают сквозную атрибуцию.

- [x] 6.1 Выполнить scoped generation и inventory: ровно 24 canonical RU/EN pages, 14 новых Astro, unchanged other-locale HTML/styling, unchanged CNAME; no secrets/QA artifacts в публичном diff.
- [x] 6.2 Через local static HTTP server проверить все 24 страницы, `/en/`, root/nested assets, crawl graph, internal links, canonical/hreflang/sitemap, exact CTA/security attributes, metadata и JSON-LD parsing/visible consistency.
- [x] 6.3 Выполнить редакторскую сверку RU/EN с актуальным master, channel/access matrix и disclaimer; удалить старые Telegram-only/«четыре Premium» claims и случайные английские подписи RU. Подтвердить самостоятельность шести Astro тем.
- [x] 6.4 Проверить rendered pages на 320/360/375/390/414/768/1024/1440 px, portrait/landscape, 200% zoom и increased text; проверить keyboard/focus/contrast/reduced motion/no-JS, отсутствие console errors/overflow/overlap и dimensions медиа. Зафиксировать representative templates и все unique content states, не ограничиваться home.
- [x] 6.5 Провести local/lab performance и asset checks, безопасные entry integration checks; оформить отчёт с separate local, application E2E и deployment-only evidence. Отсутствующие live/field результаты не объявлять PASS.

## 7. Публикация и проверки рабочего сайта

Только после выполнения 1–6 и отдельного разрешения владельца на публикацию. Необходимые действия приложения оформляются/выпускаются по собственному Taro change и его разрешениям.

- [x] 7.1 Подготовить reviewable diff/commit и rollback, проверить собственный Git root/Pages source и зафиксировать разрешение пользователя «изменяй и опубликовыывай» на публикацию сайта; не связывать её с серверным deployment другого сайта.
- [x] 7.2 После разрешения опубликовать GitHub Pages и проверить HTTPS, все 24 URL, legacy redirect, публичные assets/canonical/hreflang/sitemap/robots, mobile smoke и три entry destinations на рабочем домене.
- [x] 7.3 Подтвердить опубликованный путь source → CTA → нужный интерфейс → signup/account/referral invariants с разрешёнными тестовыми identities; при регрессии применить предусмотренный откат без ручного исправления финансов.
- [x] 7.4 Оформить итоговую матрицу проверки и инструкции Search Console/Bing URL inspection/sitemap submission. Отправку выполнять только при наличии доступа/разрешения; не блокировать достоверный отчёт отсутствием внешнего доступа и не заявлять индексацию/позиции/AI citations/field CWV без данных.

Проверки выполнены в границах verification.md: public HTTPS/menu, live Mini App launch/auth/bootstrap существующего пользователя, unit и rollback-only registrations. Создание новых живых аккаунтов, email delivery и платная referral reward не выполнялись; Search Console/Bing требуют доступа владельца. Разрешение на публикацию получено сообщением «изменяй и опубликовыывай».

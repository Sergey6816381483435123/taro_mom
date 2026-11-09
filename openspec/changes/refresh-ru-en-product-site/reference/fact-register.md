# Реестр фактов и ограничений проверки

Дата подготовки: 9 ноября 2026 года, Europe/Moscow. Исследование: локальные исходники сайта и Go-приложения, общедоступная первичная документация. БД, BotFather, персональные аккаунты и платежи не проверялись. Наличие кода не доказывает включённость функции в production.

## Источники и их приоритет

1. Решения владельца в текущем обсуждении: RU/EN, Таро главное, отдельный Астро-кластер, сохранение стиля, интерфейс продукта, три входа в заданном порядке, единая реферальная атрибуция, цены внутри продукта.
2. Подтверждённые контракты Go и актуальные публичные интерфейсы. Перед публикацией — сверка фактического каталога/настроек read-only.
3. `reference/product-description.md` — предлагаемая новая редакция опорного описания; переносится в корневой master только при реализации после сверки.
4. Действующие файлы сайта и прежние OpenSpec — свидетельства прежней версии, а не подтверждение актуального продукта.

Изменение источника истины явно согласовано пользователем: старый master и правило единственного CTA устарели. До реализации они не переписываются. Для архивных документов не исправлять историю задним числом.

## Подтверждено исходниками

Все пути Taro ниже относительно `/opt/stacks/bots/Taro`; пути сайта — относительно `/opt/stacks/sites/taro_mom`.

| Тема | Доказательство | Что разрешено проектировать / что перепроверить |
|---|---|---|
| Два направления в приложении | `go/internal/modules/webapp/postgres/catalog.go:26`, `:98` | Mini App/browser содержат Таро и Астро. Астро-бот как вход не означает приложение только об астрологии. |
| Каталог Таро динамический | `go/internal/modules/webapp/postgres/catalog.go:60` | Активность, стоимость и Premium-флаг поступают из `spread_types`. Перед публикацией проверить доступные записи; seed/migration не равны live-каталогу. |
| 14 кодов основных раскладов | `go/internal/modules/reading/format.go:13`; runners `go/internal/modules/webapp/app/tarot.go:171` | Совет карты/Рассвет, да/нет, три карты, отношения, следующий шаг, новая любовь, ближайшее будущее, возвращение, развитие, чувства, выбор A/B, работа/финансы, Кельтский крест, год. UI-названия сверить в RU/EN. |
| Карта дня и Колесо фортуны различаются | `go/internal/modules/card/README.md:1`; `go/internal/modules/wheel/README.md:8`; `catalog.go:133` | Не смешивать ежедневную карту и вращение Колеса. Не обещать бесплатный кредит за каждое вращение. |
| Уточнение и дополнительная карта | `go/internal/modules/webapp/postgres/catalog.go:153`; `go/internal/modules/reading/format.go:27` | Продолжение расклада есть; не обещать доступность каждого действия для любого результата. |
| Луна, гороскопы, натал, совместимость, транзиты, события, соляр | `go/internal/modules/webapp/postgres/catalog.go:98` | 10 feature definitions Астро; страницы группируют их по задаче, без числового обещания в рекламе. |
| Данные рождения | `go/internal/modules/webapp/postgres/catalog.go:204`, `:116` | Луна не требует персональных полей; персональные функции запрашивают недостающую дату, время, место; совместимость — данные второго человека; соляр — год и место. Не называть все поля необязательными и не обещать точный расчёт без них. |
| Условия доступа зависят от сценария | `go/internal/modules/webapp/app/access.go:87` | Луна/события/краткий портрет в коде имеют бесплатные пути; новые полные разборы и часть Astro требуют Premium/кредиты. Есть trial/replay exceptions. Нельзя выводить итоговую цену только из статического `catalog.go`. |
| Неодинаковые повторы | `access.go:126`, `:140`, `:145`, `:152` | Сохранённый результат не всегда требует новой оплаты; соляр имеет отдельную проверку Premium. Не обещать «всё ранее купленное всегда доступно без Premium». |
| Дневник | `go/README.md:57`; защищённые journal routes в `go/internal/transport/webapp/handler.go` | Настроение/энергия/заметка/история. Публичный сайт не собирает записи и данные рождения. |
| Просмотр и справка карт | `go/web/README.md`; `go/internal/transport/webapp/card_canon.go:14`; `go/web/src/canon-copy.ts` | Справка включается отдельной настройкой `show_card_canon`; не выдавать её за отдельный уже публичный SEO-справочник. |
| Telegram и email auth | `go/internal/transport/webauth/email.go:22`; `go/web/src/email-access.tsx:64`; `go/docs/email-first-registration-2026-10-30.md:3` | Браузер не требует обязательно Telegram. Новый email-аккаунт не становится тем же Telegram-аккаунтом автоматически. |
| Общее владение аккаунтом | `go/internal/modules/emailauth/postgres/merge.go:138` | Баланс/история/профиль общие у одной или явно связанных identities. Linking/merge требует подтверждения, не совпадения имени/email. |
| Адрес приложения | `go/BOTFATHER_SETUP.md:9`, `:45`; `go/ASTRO_RELEASE.md:3` | Канонический app origin в проекте — `https://app.taro.mom/`. Авторизованный сценарий в этом исследовании не выполнялся. |
| Mini App launch | `go/internal/modules/profile/service.go:43`; `go/internal/modules/profile/service.go.md:9` | Текущий профиль ведёт в `@astrology_1_bot`, затем приложение открывается кнопкой. Настройка прямого Main Mini App сейчас не подтверждена; не считать генерацию `startapp` доказательством запуска. |
| Referral и source различаются | `go/internal/transport/telegram/normalize.go:157`, `:623`; `go/internal/modules/user/postgres/start_repository.go:56`; `go/internal/modules/start/app/referral.go:42` | Нативный `/start ref<ID>` и жизненный цикл вознаграждения отделены от marketing labels. Факт бонуса проверяется отдельно от клика. |
| Пробел Mini App referral | `go/internal/modules/webauth/app/service.go:214`; `go/internal/modules/webapp/postgres/profile.go:28`; `go/internal/modules/user/postgres/web_registration.go:17` | Проверенный `start_param` записывается как source; `RegisterWeb` не получает ReferrerID. Прямой `startapp=ref...` не доказывает создание referral relationship. |
| Реферальный baseline Astro chat → Mini App | `go/internal/modules/webapp/postgres/entry.go:47`; `go/cmd/worker/web.go:229`; `go/internal/modules/user/postgres/web_registration.go:17` | Astro `/start ref...` передаёт ReferrerID в RegisterWeb и активирует Astro membership. Для нового профиля создаётся штатная связь, для existing inviter не меняется. Затем пользователь открывает приложение кнопкой; live-проверка ещё нужна. |
| Marketing redirect | `go/internal/modules/webadmin/postgres/marketing.go:13`; `go/migrations/0087_unified_admin_marketing.sql:112` | `/go/<code>` с `m_...` считает маркетинг и не заменяет обязательный referral. Не использовать его вместо точной первой CTA. |
| Browser referral gap | `go/internal/modules/webauth/app/service.go:350`; `go/internal/transport/webauth/email.go:167` | Поддержка `?ref=` в browser signup не найдена; это целевой новый контракт, а не действующий URL с доказанной атрибуцией. |
| Источник статического сайта | `sitegen/templates/{home,detail}.html`, `sitegen/content/{ru,en}.json`, `sitegen/routes.json` | 10 existing canonical RU/EN pages, ещё 18 локалей. `/en/` redirect не распространяется на `/en/<topic>/`. |
| Воспроизводимость | `.gitignore`; `tools/generate_site.py`, `tools/test_sitegen.py`, `tools/check_site.py` | Текущие инструменты находятся в игнорируемом `tools/`. При реализации версионировать только необходимые проверенные генератор/проверки; сайт остаётся статическим. |

## Конфликты, которые закрывает реализация

- Master/архив: «Telegram-only», «ровно четыре Premium-расклада», «все CTA равны одному адресу» → новый согласованный контракт. Изменять только текущие источники/проверки, не архивы.
- Текст `go/README.md:63` о прежнем Astro-доступе расходится с текущим `app/access.go:144` для новой синастрии/соляра. Публичное описание не фиксирует это условие до сопоставления исполняемого кода и рабочего каталога.
- Активное старое изменение `localize-supported-languages` описывает уже изменённые маршруты и старый состав продукта. Его существование не означает незавершённость этого proposal и не разрешает массовую регенерацию других языков.
- Количество языков, стоимость пакетов и Premium-бонусы — изменяемые данные. Старые «20», «5/10/30» и «50» не становятся обязательными claims нового сайта без свежей сверки.

## Условия перед публикацией, не вопросы владельцу

Ответственный за реализацию самостоятельно проверяет read-only: публичные entry URLs, действующий способ Mini App launch, enabled каталог и язык RU/EN, free/paid/Premium-правила, legal/support destinations. Технические неизвестные закрываются исследованием и тестами. При отсутствии доказательства — не публиковать утверждение как факт; сохранить соответствующий выпускной пункт невыполненным. Для атрибуции трёх входов сокращение согласованного объёма не допускается.

## Сверка перед выпуском, 9 ноября 2026

Этот раздел обновляет статусы подготовительного исследования выше. Пользователь разрешил реализацию и публикацию сообщением «изменяй и опубликовыывай».

- Read-only БД `taroshenka`, TLS verify-full: schema104 до выпуска, 20 включённых языков, 15 активных типов раскладов; Premium: celtic_cross/year/choice/work_finance/what_next/feelings. Карта дня имеет нулевую стоимость, остальные цены на сайт не переносятся. Наличие типа в БД отдельно от доступности Daily Card в интерфейсах: обещание бесплатно относится к основному Telegram-боту.
- Telegram Bot API getMe подтвердил `taroshenka_bot` и `astrology_1_bot`. getChatMenuButton для Astro вернул `web_app` с `https://app.taro.mom/`; Main Mini App не включён. Поэтому сохранён двухшаговый `/start ref...` → кнопка. Для основного бота menu type `commands`.
- Support URL `https://t.me/taroshenka_support_bot` подтверждён конфигурацией продукта. Не найдены подтверждённые самостоятельные privacy/terms destinations, поэтому вымышленные страницы не добавлены. Дисклеймер опубликован полностью. Оплата описана без универсальных обещаний способов/сумм; конкретные средства показываются в интерфейсе продукта.
- Browser referral реализован отдельным Taro change `add-browser-referral-attribution`: миграция105, worker r75. Проверены server pending/secure opaque cookie/first-valid 30дней публичным HTTPS запросом. Только тестовая pending запись удалена по точному hash после проверки.
- OIDC/email carryover, new/existing/link/reset/expiry/replay покрыты unit-тестами; сохранение referral/new registration/welcome grant и merge restrictions — пятью rollback-only DB тестами. Пользователи, балансы, ledger, платежи, subscriptions и spreads по before/after aggregates не изменились. Новые реальные аккаунты, отправка email и финансовое вознаграждение в production не создавались; это граница live E2E.
- Независимые code/SQL reviews пройдены. Блокировки active inviter `FOR SHARE` согласуют регистрацию с merge; merge отклоняет joined referral связи. Обычный reward lifecycle остаётся отдельным от pending и маркетинга.
- Выпуск сохранил точный frontend r74, env/mounts/routes/networks/host configuration и остальные контейнеры. Предыдущий worker r74 сохранён для отката; schema105 обратно не удаляется при rollback worker.
- Полный новый master находится в корне сайта; прежнее описание и правило единственной CTA заменены только в текущих документах, архивы сохранены.

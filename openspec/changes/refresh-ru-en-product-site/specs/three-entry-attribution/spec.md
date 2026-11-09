## ADDED Requirements

### Requirement: Реестр входов задаёт точные назначения
Все 24 страницы SHALL использовать порядок: Тарошенька → Астро Mini App → browser. Первый conversion URL MUST в точности равняться `https://t.me/taroshenka_bot?start=ref974025936`, без `/go`, сокращателя, JS redirect и дополнительных query parameters. Baseline второго SHALL быть `https://t.me/astrology_1_bot?start=ref974025936` с пояснением запуска Mini App кнопкой. Третий SHALL быть `https://app.taro.mom/?ref=974025936` только после реализации подтверждённой browser attribution. `target=_blank` SHALL сопровождаться `rel="noopener noreferrer"`.

#### Scenario: Статическая сверка ссылок
- **GIVEN** готов весь набор RU/EN HTML и JSON-LD
- **WHEN** validator классифицирует conversion/identity/internal links
- **THEN** первая conversion ссылка точна, второй/третий target соответствуют реестру, а plain bot identities не используются вместо conversion

### Requirement: Mini App запускается поддерживаемым способом с сохранением referral
Astro `/start ref974025936` SHALL использовать штатную регистрацию нового профиля с inviter, затем открывать приложение существующей Telegram-кнопкой. Сайт MUST честно объяснять двухшаговый путь. Прямой `startapp` MUST NOT использоваться без доказанной настройки Main Mini App и создания referral relationship из проверенного Telegram start_param. Поддержка marketing `m_...` MUST NOT считаться эквивалентом referral.

#### Scenario: Новый пользователь пришёл через Астро
- **GIVEN** Telegram identity ещё не имеет canonical account и inviter валиден
- **WHEN** пользователь нажимает Start по Astro referral link и затем открывает Mini App
- **THEN** создана одна штатная referral relationship с `974025936`, приложение открывается под тем же аккаунтом, а ссылка не ведёт в основной bot вместо Astro

#### Scenario: Прямой Main Mini App не подтверждён
- **GIVEN** конфигурация прямого запуска неизвестна либо start_param не создаёт relationship
- **WHEN** выбирается второй CTA
- **THEN** используется проверяемый двухшаговый baseline, а не предположительно действующий `startapp`

### Requirement: Browser referral переживает регистрацию и вход
В отдельном Taro change browser SHALL принимать публичный `ref=974025936`, валидировать inviter и сохранять первый валидный pending ref на 30 дней серверным first-party механизмом. Новая valid ссылка в этом окне MUST NOT перезаписывать ref; invalid ref MUST NOT стирать valid pending или блокировать вход. Pending SHALL переживать Telegram OAuth и email verification/password creation, включая письмо на другом устройстве через серверный registration intent. Referral SHALL создаваться атомарно с новым подтверждённым canonical account; сам query/click MUST NOT создавать аккаунт или бонус.

#### Scenario: Email verification на другом устройстве
- **GIVEN** новый посетитель пришёл по browser referral и начал email-first signup
- **WHEN** подтверждает ещё действующее письмо на другом устройстве и создаёт пароль
- **THEN** inviter берётся из серверного intent с соблюдением срока, создаётся одна relationship, а raw ref не является подтверждением личности

#### Scenario: Повторный переход с другим ref
- **GIVEN** valid pending ref ещё действует
- **WHEN** до создания аккаунта пришла другая или повреждённая метка
- **THEN** сохраняется первый valid ref; после истечения pending новая valid метка может начать новое окно, но не меняет inviter существующего аккаунта

### Requirement: Identity и финансовая история не перепривязываются
Existing accounts SHALL сохранять inviter и referral history, включая отсутствие inviter; новый рекламный переход MUST NOT присваивать им inviter задним числом. Self-referral/несуществующий inviter SHALL отвергаться без нарушения входа. Retry/concurrent callback SHALL быть идемпотентным. Linking/merge SHALL сохранять подтверждение identities и текущие инварианты владения; конфликт referral histories MUST NOT разрешаться тихой перепривязкой или повторной выплатой. Если безопасное штатное слияние невозможно, операция SHALL явно отклоняться, сохраняя аккаунты.

#### Scenario: Existing Telegram account входит через browser referral
- **GIVEN** canonical account уже создан, независимо от наличия inviter
- **WHEN** пользователь проходит OAuth по referral URL
- **THEN** он входит в свой аккаунт без изменения inviter, history, credits и Premium; новый signup/reward не создаётся

#### Scenario: Callback повторился или linking конфликтует
- **GIVEN** signup уже завершился либо identities имеют несовместимые referral histories
- **WHEN** повторяется запрос или подтверждается linking
- **THEN** signup не дублируется; допустимый merge сохраняет штатные инварианты, а недопустимый отклоняется без потери данных

### Requirement: Referral lifecycle отделена от маркетинговой аналитики
Click/source/campaign labels SHALL храниться отдельно от пользовательской referral relationship. Точное первое CTA MUST NOT заменяться marketing `m_...`. Reward SHALL следовать действующему доменному событию первого сохранённого основного расклада, а не клику, логину или любой Astro-операции. Использование одного eligible события через chat/Mini App/browser SHALL быть идемпотентным. Сайт MUST NOT обещать сумму или гарантировать бонус существующему пользователю.

#### Scenario: Источник записан без реферальной связи
- **GIVEN** в marketing/source есть метка referral либо учтён `/go` click
- **WHEN** оценивается выполнение требования всех трёх входов
- **THEN** без доказательства relationship и штатного eligible reward lifecycle проверка считается неуспешной

### Requirement: Сквозное доказательство является условием публикации
Выпуск SHALL требовать отдельной проверки каждого из трёх входов: нового/существующего account, invalid/self ref, повторов и сохранения финансов/истории. Browser SHALL дополнительно проверить OAuth/email, TTL, first-valid policy и linking; Mini App — реальный Telegram initData/кнопку launch. Проверки SHALL использовать только разрешённые тестовые identities и fixtures/rollback для финансовых эффектов. Реальные покупки, ручные бонусы и production-записи MUST NOT выполняться под видом этапа подготовки. Отсутствие Taro dependency SHALL блокировать публикацию полного обновления, не приводя к удалению третьего входа.

#### Scenario: Browser URL открывается, но ref теряется после OAuth
- **GIVEN** static/link smoke пройден
- **WHEN** E2E выявляет потерю referral при регистрации
- **THEN** выпускной пункт остаётся невыполненным и сайт не объявляется готовым к публикации; согласованный объём трёх входов сохраняется

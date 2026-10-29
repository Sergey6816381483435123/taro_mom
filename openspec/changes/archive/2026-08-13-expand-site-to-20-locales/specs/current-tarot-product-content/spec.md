## ADDED Requirements

### Requirement: Все locale утверждают поддержку 20 языков
Каждая home, FAQ, metadata и structured-data формулировка о языках SHALL утверждать поддержку 20 языков и SHALL представлять полный canonical catalog. Система MUST NOT содержать пользовательские утверждения про восемь языков или старый список только из `en`, `ru`, `de`, `es`, `fr`, `hi`, `pt`, `tr`.

#### Scenario: Поиск устаревшего language claim
- **GIVEN** source и generated output готовы
- **WHEN** validator ищет числовые и словесные варианты fixed-eight claims и сравнивает language lists
- **THEN** устаревших утверждений нет, а каждый visible catalog содержит 20 подтверждённых locales

### Requirement: Четыре Premium-расклада описаны последовательно
Home reading catalog, Premium section, FAQ, related copy, metadata и JSON-LD SHALL учитывать: Choice Between Two Options — Premium, 7 карт; Work & Finances — Premium, 7 карт; Celtic Cross — Premium, 10 карт; Year Ahead — Premium, 12 карт. Choice SHALL описывать симметричное сравнение A/B и критерий самостоятельного решения; Work & Finances SHALL описывать ситуацию, ресурсы, ограничения, возможные действия и ближайшее направление без обещания дохода.

#### Scenario: Проверка Premium matrix
- **GIVEN** любой locale dictionary и rendered home
- **WHEN** semantic validator читает Premium entries
- **THEN** присутствуют ровно четыре подтверждённых reading definitions с правильным количеством карт и безопасным смыслом

### Requirement: Остальная продуктовая матрица остаётся полной
Контент SHALL также отражать Daily Card, Yes or No, three-card spread, Dawn, five-card relationship reading, additional card, contextual follow-up, completed-reading history и profile с name, birth date, zodiac sign, saved language и selected deck. Система MUST NOT обещать конкретную недоступную deck, включая Visconti.

#### Scenario: Product matrix сверяется с master description
- **GIVEN** локализованный контент готов
- **WHEN** content checklist сравнивается с `taro-bot-website-master-description.md`
- **THEN** все обязательные функции присутствуют по смыслу, а неподтверждённых функций и deck promises нет

### Requirement: Credits, Premium и оплаты описаны без устаревающей цены
Каждая locale SHALL сообщать о packages 5, 10 и 30 credits, monthly Premium, 50 credits при подключении и ещё 50 после успешного ежемесячного продления. Current price, currency, payment method и subscription terms SHALL направляться в bot before purchase. Russian copy MAY сообщать о YooKassa card/SBP и Telegram Stars; остальные 19 locales SHALL сообщать о Telegram Stars. Exact universal price и публичный DOT MUST NOT появляться.

#### Scenario: Проверка payment copy
- **GIVEN** locale равен `ru` или одной из остальных 19 локалей
- **WHEN** validator проверяет соответствующий payment variant
- **THEN** указан разрешённый channel-specific смысл без точной цены, DOT или внутренних payment details

### Requirement: Conversion CTA сохраняют referral attribution
Каждая conversion CTA SHALL иметь точный `href="https://t.me/taroshenka_bot?start=ref974025936"`; при `target="_blank"` SHALL присутствовать `rel="noopener noreferrer"`. Plain `https://t.me/taroshenka_bot` SHALL использоваться только для identity reference и `sameAs`.

#### Scenario: Проверка Telegram links
- **GIVEN** все 100 pages сгенерированы
- **WHEN** validator классифицирует каждый Telegram URL как conversion или identity
- **THEN** conversion links полностью сохраняют referral parameter, username не изменён, а identity links не используются вместо CTA

### Requirement: Safety positioning и полный disclaimer присутствуют в каждой локали
Каждая locale SHALL позиционировать Tarot как entertainment, symbolic interpretation и self-reflection. Видимый disclaimer SHALL сообщать, что readings и AI interpretations не являются reliable prediction, не заменяют medical, psychological, legal, financial или другую professional help и оставляют важные решения пользователю. Контент MUST NOT обещать guaranteed future, correct decision, mind reading, partner return, income или financial success.

#### Scenario: Проверка safety content
- **GIVEN** локализованная page готова
- **WHEN** semantic checklist и запрещённые-claim scans проверяют dictionary и rendered output
- **THEN** обязательные disclaimer concepts присутствуют, а запрещённых обещаний нет

### Requirement: Меняющиеся факты имеют честную provenance
Product content SHALL ссылаться на обновлённый `taro-bot-website-master-description.md` как repo source of truth. Отчёт SHALL отмечать, что live PostgreSQL/n8n проверка не выполнялась, а 20 locales и четыре Premium readings подтверждены пользователем 13 августа 2026 года. Implementation MUST NOT изменять соседний bot repository.

#### Scenario: Формирование итогового отчёта
- **GIVEN** локальная реализация завершена
- **WHEN** создаётся verification report
- **THEN** он различает подтверждённые пользователем факты, локально проверенные свойства сайта и недоступные live/deployment проверки

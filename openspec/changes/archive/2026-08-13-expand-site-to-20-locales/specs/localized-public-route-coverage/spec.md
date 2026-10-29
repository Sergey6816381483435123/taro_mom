## ADDED Requirements

### Requirement: Все существующие типы публичных страниц покрыты 20 локалями
Система SHALL публиковать для каждой из 20 локалей home, Daily Card, Yes or No, three-card spread и relationship reading. Canonical matrix SHALL содержать ровно 100 страниц; `en/index.html` legacy redirect SHALL учитываться отдельно и MUST NOT считаться canonical page.

#### Scenario: Проверка route matrix
- **GIVEN** сайт сгенерирован
- **WHEN** coverage validator сопоставляет 20 locales и 5 route keys
- **THEN** существуют ровно 100 canonical files без пропусков и дублей

### Requirement: Каждая страница полностью локализована
Header, footer, navigation, mobile menu, language selector, hero, badges, CTA, sections, breadcrumbs, reading cards, Premium labels, related links, FAQ, disclaimer, `title`, descriptions, Open Graph/Twitter metadata, JSON-LD, `alt`, `aria-label`, visually hidden и skip-link text SHALL быть представлены на языке документа. Исключениями являются brand, username, URL и технические identifiers.

#### Scenario: Поиск чужого пользовательского текста
- **GIVEN** locale не является `en` или `ru`
- **WHEN** проверка анализирует source dictionary и rendered HTML
- **THEN** в обязательных полях нет английского или русского fallback-текста, кроме явного allowlist собственных имён и технических значений

### Requirement: Языковой переключатель содержит 20 native labels
Каждая canonical page SHALL содержать доступные реальные ссылки на эквивалент текущего route во всех 20 локалях в каноническом порядке. Переключение MUST сохранять route key и MUST NOT отправлять detail page на home, если эквивалент существует.

#### Scenario: Переключение языка с detail page
- **GIVEN** пользователь находится на relationship reading
- **WHEN** он выбирает العربية
- **THEN** ссылка ведёт на арабский relationship route, а не на арабскую главную

### Requirement: Арабская и персидская локали работают справа налево
Документы `ar` и `fa` SHALL иметь корректные `lang` и `dir="rtl"`; остальные документы SHALL иметь `dir="ltr"`. Menu, selector, icons, cards, breadcrumbs, CTA и responsive layout MUST оставаться читаемыми и управляемыми на mobile и desktop без логических ошибок направления.

#### Scenario: RTL на узком экране
- **GIVEN** арабская или персидская страница открыта при 320 CSS px
- **WHEN** пользователь просматривает меню, hero, cards, FAQ и CTA
- **THEN** отсутствуют horizontal overflow, clipping и overlap, порядок чтения корректен, а interactive targets остаются доступными

### Requirement: Страницы доступны без JavaScript и адаптивны от 320 px
Основной контент, locale navigation, CTA и links SHALL быть обычным server-delivered HTML. Все pages SHALL сохранять usability при ширинах 320, 360, 375, 390, 414, 768, 1024 и 1440 px, browser zoom, increased text, keyboard navigation и reduced motion.

#### Scenario: JavaScript отключён
- **GIVEN** JavaScript не выполняется
- **WHEN** пользователь открывает любую canonical page
- **THEN** он может прочитать весь важный контент, выбрать язык, перейти к related page и открыть Telegram CTA

### Requirement: Существующие визуальные assets переиспользуются безопасно
Значимые изображения SHALL иметь real `src`, explicit dimensions и локализованный concise `alt`; decorative images SHALL иметь пустой `alt`. Root-absolute asset paths SHALL работать с home и nested detail routes. Reference images MUST NOT изменяться или публиковаться как тяжёлые page backgrounds.

#### Scenario: Проверка assets с nested route
- **GIVEN** страница открыта по двухуровневому locale/detail URL
- **WHEN** валидатор разрешает каждый local asset URL от корня сайта
- **THEN** все assets существуют с точным регистром, а изображения имеют width, height и допустимый alt

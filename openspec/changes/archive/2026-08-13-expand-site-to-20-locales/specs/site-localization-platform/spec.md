## ADDED Requirements

### Requirement: Канонический каталог содержит ровно 20 локалей
Система SHALL хранить один машиночитаемый каталог locale codes в порядке `en`, `ru`, `id`, `ms`, `de`, `es`, `fr`, `it`, `nl`, `uz`, `pl`, `pt`, `tr`, `be`, `uk`, `kk`, `ar`, `fa`, `ko`, `hi`. Каждая запись SHALL содержать подтверждённый native label, направление, public segment, `hreflang`, `og:locale` и home URL; routing, selector, generator, sitemap и tests SHALL читать этот каталог, а не собственные allowlist.

#### Scenario: Проверка каталога локалей
- **GIVEN** исходники локализации готовы к генерации
- **WHEN** валидатор читает каталог и ищет locale allowlists в остальных source-файлах
- **THEN** он находит ровно 20 уникальных записей в заданном порядке и не находит конкурирующего fixed-eight или иного списка

### Requirement: Нормализация locale воспроизводит контракт бота
Система SHALL нормализовать locale до lowercase base tag, SHALL разрешать `pt-BR` в `pt` и SHALL разрешать неизвестное, пустое, `NULL` или отключённое значение в `en`. Диагностический fallback содержимого SHALL иметь порядок requested → `en` → `ru`, но release generation MUST завершаться ошибкой при fallback из-за отсутствующего перевода.

#### Scenario: Входной locale имеет регион
- **GIVEN** нормализатор получает `pt-BR`
- **WHEN** он выбирает запись каталога
- **THEN** результатом является canonical locale key `pt`

#### Scenario: Перевод отсутствует при release generation
- **GIVEN** ключ существует в English schema, но отсутствует в целевой локали
- **WHEN** запускается release generation или `--check`
- **THEN** процесс завершается ненулевым кодом с locale, route и key и не подменяет значение fallback-текстом

### Requirement: Все словари имеют одну строгую схему
Каждый locale SHALL иметь ровно один словарь и одинаковый канонический набор ключей для общего UI, home и четырёх detail route types. Missing, blank, extra или неверно типизированные значения MUST блокировать генерацию. Наборы interpolation placeholders и разрешённых inline tokens SHALL совпадать между локалями.

#### Scenario: В переводе потерян placeholder
- **GIVEN** English value содержит `{count}`, а перевод не содержит этот token
- **WHEN** запускается проверка схемы
- **THEN** проверка завершается ошибкой и точно указывает locale и translation key

### Requirement: Генерация статического сайта детерминирована
Локальный генератор SHALL использовать Python 3 standard library, SHALL создавать deployable HTML/CSS/JS и `sitemap.xml` без runtime dependency и SHALL давать одинаковый byte output при одинаковых sources. Generated output SHALL быть закоммичен и SHALL работать на GitHub Pages без выполнения генератора.

#### Scenario: Повторная генерация чистого дерева
- **GIVEN** generated files соответствуют source manifests, templates и dictionaries
- **WHEN** выполняется `python tools/generate_site.py --check`
- **THEN** команда успешна и не изменяет рабочее дерево

### Requirement: Drift между sources и output блокирует выпуск
Система SHALL проверять, что каждый generated public file совпадает с текущей повторной генерацией, и MUST перечислять отсутствующие, лишние и изменившиеся generated paths.

#### Scenario: HTML отредактирован вручную
- **GIVEN** пользователь изменил generated HTML без изменения словаря или шаблона
- **WHEN** запускается drift check
- **THEN** проверка завершается ошибкой и предлагает исправить source либо повторно сгенерировать output

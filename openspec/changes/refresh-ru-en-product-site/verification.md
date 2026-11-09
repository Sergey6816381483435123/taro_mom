# Проверка реализации и выпуска

Дата: 9 ноября 2026 года, Europe/Moscow. Пользователь разрешил реализацию и публикацию сообщением «изменяй и опубликовыывай». Новые вопросы владельцу не требуются. Этап на момент этого коммита: локальная проверка завершена, публикация и проверка домена — следующий шаг.

Результат: обновлены 10 существующих RU/EN страниц и добавлены 14 Astro, всего 24 canonical URL. Таро остаётся главным направлением. Три входа расположены в согласованном порядке в начале и конце каждой страницы. Тексты, FAQ, metadata, JSON-LD и полный дисклеймер согласованы с новым корневым master. Цена и требования показываются в продукте.

| Проверка | Результат |
|---|---|
| OpenSpec strict validation | PASS: proposal/design/5 specs/tasks, 30 требований и 33 сценария |
| `python3 sitegen/generate.py --check` | PASS: 24 страницы, воспроизводимость из tracked source |
| `python3 sitegen/validate.py` | PASS: 24 страницы, 14 новых Astro, 1014 ссылок, 26 img elements, 114 sitemap URLs |
| Scope/integrity | PASS: 97 защищённых файлов совпали, включая 90 других locale HTML, 3 общих legacy CSS, 2 прежних шаблона, CNAME и `/en/` redirect |
| Sitemap старых локалей | PASS: 90 записей семантически совпадают с HEAD до изменения; lastmod меняется только для 24 RU/EN |
| Метаданные и обнаружение | PASS: self canonical, existing20-locale clusters, AstroRU/EN/x-default; `/en/` исключён из canonical cluster; JSON-LD parsing и 3 action targets; robots/GPTBot policy сохранены |
| Browser static HTTP | PASS: все24страницы на 320/360/375/390/414/768/1024/1440px, landscape844×390, 200% CSS layout zoom на768px, root text125% на320px — всего264случая |
| Без JavaScript | PASS: 24 страницы, тексты/FAQ/три входа доступны |
| Клавиатура и motion | PASS: skip link перемещает фокус на main; видимый фокус ссылок/summary; reduced-motion отключает плавную прокрутку |
| Контраст основных токенов | PASS: проверено6пар, минимальный ratio9.47:1; это проверка использованных основных цветов, не полный аудит WCAG |
| Геометрия/ресурсы/ошибки | PASS: нет horizontal overflow/offscreen text or controls, ошибок консоли или HTTP; размеры изображений заданы, lazy images загружаются |
| Изображения | PASS: 6 WebP реального UI r74/r75 с демонстрационными данными, 37–75KB; hero WebP≈123KB, существующая иллюстрация. Проверены RU/EN тексты и card viewer, происхождение и SHA256 в product-images.json |
| Визуальная проверка | Главные и representative detail/overview страницы просмотрены; итоговые первые экраны4типов на320/390/1440px проверены отдельно после исправления кадрирования hero |
| Local lab performance | HTML12810–24494bytes; локальный Chromium LCP24–564ms. Это локальные замеры на тестовой машине, не полевые CWV или обещание публичной скорости; INP не измерялся |
| Независимый review | Code reviewer не нашёл release blockers в генераторе/контенте/CSS/маршрутах/master/sitemap; браузерный вывод проверен основным агентом |
| `git diff --check` | PASS |

Приложение: отдельный Taro change `add-browser-referral-attribution`, commit `03627e0`, schema105, worker `browser-referral-20261109-r75`. Unit packages и пять rollback-only DB тестов PASS. Публичный HTTPS browser capture/first-valid/TTL30дней/Secure HttpOnly Lax проверен; тестовая pending запись удалена по точному hash. User/financial aggregates неизменны. Точные frontend assets совпали с r74; env/mounts/routes/networks/host config и остальные контейнеры сохранены. Live Bot API подтвердил usernames обоих ботов и Astro menu Web App URL. Подробности и границы — verification отдельного Taro change.

Не выполнялись: создание реальных новых аккаунтов, доставка email, запуск Telegram от лица пользователя и платная referral reward. Регистрации проверены unit-фейками и rollback-only DB, публичный capture — настоящим HTTPS. Это не полная сквозная пользовательская приёмка трёх каналов.

Локальные QA screenshots, browser reports, venv и browser libraries находятся вне public diff, в `/tmp/taro-site-qa` и временных каталогах. На сайт входят только шесть предназначенных для публикации UI изображений и WebP hero. Нет site backend, forms, analytics, новых JavaScript или секретов.

## Публикация

Ожидается fast-forward push в собственный `origin/main` GitHub Pages репозитория `Sergey6816381483435123/taro_mom`, CNAME `taro.mom`. Предыдущий remote commit `b384d9dcab687f58db6b5505fc24e62386418559`; до этого изменения локальный HEAD `03bfcf19cd17dfe9df20ce77513f561c0ae100ad`. Откат сайта — обратный коммит выпуска и обычный push после локальной проверки; force push не нужен. Публикация не связана с другими сайтами хоста.

После build требуется проверить все24URL и публичные assets/metadata/robots/sitemap, `/en/`, HTTPS и mobile smoke. Статус внешних сервисов: Search Console/Bing submission и URL inspection не выполнены, права доступа не подтверждены. Владелец может отправить `https://taro.mom/sitemap.xml` в оба сервиса и проверить главные и representative AstroURL. Индексация, поисковые позиции, AI citations и field CWV не заявляются как достигнутые.

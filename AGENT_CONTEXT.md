# Контекст для AI-агента (Yarcoffee)

Файл для продолжения работы в новом чате. Репозиторий: [kurbanovvgit-creator/yarcoffeweb](https://github.com/kurbanovvgit-creator/yarcoffeweb).

## Проект

- **Yarcoffee** — витринный сайт кофейни (Ашхабад), Django 5.2, SQLite, без e-commerce.
- Стек: Django templates, `static/css/site.css`, vanilla `static/js/main.js`, `django-modeltranslation` (tk/ru/en).
- Локальный путь: `d:\company_projects\yarcoffee`
- Деплой: `deploy/PYTHONANYWHERE.md`

## Что сделано в сессии (май 2026)

### 1. Мобильное меню (бургер)

**Проблема:** нельзя закрыть меню; контент страницы (форма контактов) просвечивал; две кнопки закрытия (бургер→крестик + «×») накладывались.

**Решение:**
- `templates/components/navbar.html` — меню и backdrop **вынесены из `<header>`** (отдельные sibling-элементы).
- `static/js/main.js` — `setMobileMenu()`, класс `body.is-nav-open`, Escape, клик по backdrop, одна кнопка (бургер).
- `static/css/site.css` — z-index: backdrop 240, panel 250, nav при открытии 260; `pointer-events: none` когда закрыто; панель `translateX` справа.

### 2. Блоки преимуществ (features)

- SVG-иконки: `templates/components/feature_icon.html` (cup, wifi, beans, heart, clock, leaf).
- Уменьшены отступы/шрифты в `.feature` (`site.css`).
- Подключено в `templates/pages/home.html` и `about.html`.

### 3. Google Maps (контакты)

**Проблема:** карта не работала; старый OpenStreetMap; длинный embed обрезался в БД (`URLField` max 200).

**Решение:**
- `apps/core/maps.py` — константа `DEFAULT_MAP_EMBED_URL` (официальный embed ÝARcoffee от пользователя), `DEFAULT_MAP_OPEN_URL`, хелперы `map_iframe_src`, `map_open_url`, `map_search_query`.
- `apps/core/models.py` — `map_embed_url` **max_length=500**, default = embed ÝARcoffee; свойства `map_iframe_src`, `map_open_url`, метод `map_search_query`.
- Миграция: `apps/core/migrations/0003_widen_map_embed_url.py`.
- `templates/pages/contacts.html` — карта в левой колонке (не внутри `<form>`), iframe с `referrerpolicy="no-referrer-when-downgrade"`, ссылка «Открыть в Google Maps» (`tr.open_in_maps`).
- `seed_demo` записывает `DEFAULT_MAP_EMBED_URL` в настройки.

**Embed URL (ÝARcoffee):** см. `DEFAULT_MAP_EMBED_URL` в `apps/core/maps.py`.

### 4. Секция Our team

- Убрана с `templates/pages/about.html`.
- `apps/core/views.py` — убран запрос `TeamMember` для about.
- Модель и админка **остались** (данные в БД не трогали).

### 5. Мелочи

- `menu-tabs` — горизонтальный скролл на мобилке.
- `menu-card-grid` — 1 колонка на `<640px`.
- i18n: `nav_close`, `open_in_maps` в `apps/core/i18n.py`.
- Версия ассетов в `templates/base.html`: `?v=17` (css/js).

## Важные файлы

| Область | Файлы |
|--------|--------|
| Карта | `apps/core/maps.py`, `models.py` (SiteSettings), `contacts.html` |
| Меню | `navbar.html`, `main.js`, `site.css` (`.nav__mobile`, `.is-nav-open`) |
| About | `about.html`, `views.py` (без team) |
| Иконки | `feature_icon.html` |

## Команды

```bash
python manage.py migrate
python manage.py seed_demo          # обновит map_embed_url и демо-контент
python manage.py runserver
```

Если карта пустая в iframe (блокировка Google в сети) — работает ссылка `map_open_url` / «Открыть в Google Maps».

## Не делалось / открытые вопросы

- Push на GitHub — после создания этого файла (см. последний коммит).
- Точный адрес в админке можно уточнить в **Настройки сайта → Адрес** и **Карта (embed URL)**.
- README на GitHub ещё упоминает team на `/about/` — при желании обновить README.

## Git remote

```
origin  https://github.com/kurbanovvgit-creator/yarcoffeweb
```

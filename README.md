# Yarcoffee · Premium coffee shop website

A modern, fully offline-ready Django site for **Yarcoffee** (Ашхабад, Туркменистан) — a small specialty coffee bar with a big heart. The design is inspired by premium coffee brands like Onyx Coffee Lab, with a luxury / minimal feel, smooth animations, and a custom black / cream / coffee-brown palette.

> This is a **brand showcase site**, not an e-commerce store — no cart, no checkout, no purchase buttons.

---

## Stack

- **Backend:** Django 5.2 (Python 3.10+)
- **DB:** SQLite (file-based, zero-config)
- **Translations:** `django-modeltranslation` with TM/RU/EN model fields
- **Frontend:** plain HTML + Django templates, custom CSS (`static/css/site.css`), a local copy of Tailwind CSS as a utility layer, and vanilla JS
- **Fonts:** Inter (sans) + Cormorant Garamond (display), self-hosted
- **Images:** curated Unsplash photos pre-downloaded to `static/images/`
- **Admin:** Django admin restyled into a premium dark UI (`static/css/admin.css`)

Everything lives inside the project — no CDN, no internet required at runtime.

---

## Project structure

```
yarcoffee/
├── manage.py
├── requirements.txt
├── yarcoffee_site/         # Django project (settings, root URLs)
├── apps/
│   ├── core/               # Site settings, hero, story, team, reviews, features, contact form
│   ├── menu/               # Drink categories & drinks
│   ├── gallery/            # Masonry gallery images
│   └── dashboard/          # Custom admin branding + dashboard stats
├── templates/
│   ├── base.html
│   ├── components/         # navbar, footer, loader, lightbox, drink card
│   ├── pages/              # home, menu, about, contacts, gallery
│   └── admin/              # base_site.html, index.html (admin overrides)
├── static/
│   ├── css/                # site.css, admin.css, fonts.css, tailwind.css
│   ├── js/                 # main.js
│   ├── fonts/              # Inter + Cormorant Garamond .woff2
│   ├── images/             # logo and offline site photos
│   └── icons/              # favicon.svg
└── media/                  # optional admin uploads during development
```

---

## Quick start

```bash
# 1. Create + activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # PowerShell on Windows
# source .venv/bin/activate       # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download Tailwind, fonts & curated Unsplash images (one-time, ~30 MB)
python manage.py setup_assets

# 4. Apply migrations & seed demo content
python manage.py migrate
python manage.py seed_demo

# 5. Create an admin user
python manage.py createsuperuser

# 6. Run the dev server
python manage.py runserver
```

Open <http://127.0.0.1:8000/> for the site and <http://127.0.0.1:8000/admin/> for the dashboard.

> If your terminal has trouble with Unicode output on Windows, run once:
> ```
> $env:PYTHONUTF8="1"; $env:PYTHONIOENCODING="utf-8"
> ```

---

## Management commands

| Command | Purpose |
| --- | --- |
| `python manage.py setup_assets` | Download Tailwind, fonts, and curated Unsplash images |
| `python manage.py setup_assets --force` | Re-download everything (overwrites existing files) |
| `python manage.py setup_assets --skip-images` | Only download CSS + fonts |
| `python manage.py seed_demo` | Populate the DB with sample content (idempotent) |
| `python manage.py sync_translations` | Fill TM/RU/EN modeltranslation fields from demo content |

---

## Admin — what you can manage

The admin is at `/admin/` and is restyled to match the site.

- **Сайт · Контент**
  - Настройки сайта (singleton) — название, слоган, контакты, соцсети, embed карты, текст футера
  - Hero · слайды — фон, заголовок, подзаголовок, CTA
  - История · блоки — двухколоночные секции (текст + фото)
  - Команда — фото + роль + био
  - Отзывы — рейтинг, текст, аватар
  - Преимущества — иконка + название + описание
  - Заявки — формы из контактной страницы (read-only)
- **Меню**
  - Категории напитков
  - Напитки — фото, описание, цена, теги, флаги «новинка» / «на главной»
- **Галерея**
  - Изображения с категорией и размером плитки (1×1, 1×2, 2×1, 2×2)

The dashboard index page shows quick KPI cards for each model.

---

## Page routes

| Route | View |
| --- | --- |
| `/` | Home — hero, marquee, story, features, reviews, CTA |
| `/about/` | About — story blocks, values, team, interior |
| `/contacts/` | Contacts — info, contact form, embedded map |
| `/menu/` | Menu — categorised drink list |
| `/gallery/` | Gallery — masonry grid with lightbox |
| `/admin/` | Custom dark admin |

---

## Design system

- **Palette:** `#0d0a08` (ink), `#f5efe6` (paper), `#fbf6ec` (cream), `#4a2f1b` (coffee), `#c69753` (gold)
- **Typography:** Cormorant Garamond (display) + Inter (sans)
- **Tokens:** see `:root` block in `static/css/site.css`
- **Animations:** scroll reveal (`IntersectionObserver`), letter-by-letter (`[data-split]`), hover transitions, image zoom, marquee, custom loader
- **Accessibility:** focus styles, keyboard lightbox, semantic HTML, alt text on images

---

## License

Project is built for the Yarcoffee brand. Code is provided as-is for internal use.

"""Populate the database with rich demo content for Yarcoffee.

Run after setup_assets so the drinks/gallery have real photographs:

    python manage.py setup_assets
    python manage.py seed_demo

Re-running is safe -- every entity is upserted by a stable key.
"""

from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from apps.core.models import (
    Feature,
    HeroSlide,
    Review,
    SiteSettings,
    StorySection,
    TeamMember,
)
from apps.gallery.models import GalleryImage
from apps.menu.models import Drink, DrinkCategory


def _img_path(relative: str):
    """Return relative image path if the static image exists."""
    full = Path(settings.STATICFILES_DIRS[0]) / "images" / relative
    return relative if full.exists() else None


class Command(BaseCommand):
    help = "Seed demo content for the Yarcoffee site."

    def handle(self, *args, **opts):
        # Seed data is written in Russian first; sync_translations can then fill
        # the TM/EN modeltranslation fields deterministically.
        with translation.override("ru"):
            self._site_settings()
            self._hero()
            self._story()
            self._features()
            self._categories_and_drinks()
            self._team()
            self._reviews()
            self._gallery()
        self.stdout.write(self.style.SUCCESS("[OK] Demo content seeded."))

    def _site_settings(self):
        ss = SiteSettings.get_solo()
        ss.brand_name = "Yarcoffee"
        ss.tagline = "Маленькая кофейня с большим сердцем"
        ss.phone = "+993 65 72 25 25"
        ss.email = "hello@yarcoffee.tm"
        ss.address = "Ашхабад, Туркменистан"
        ss.address_secondary = "Каждый день · 07:30 — 22:45"
        ss.working_hours = "Каждый день · 07:30 — 22:45"
        ss.instagram = "https://www.instagram.com/yarcoffee.tm/"
        ss.tiktok = "https://www.tiktok.com/@yarcoffee.tm"
        ss.footer_note = "Crafted with love. Brewed for the neighbourhood."
        ss.save()
        self.stdout.write("  -- site settings updated")

    def _hero(self):
        defaults = {
            "eyebrow": "Specialty · Ashgabat",
            "subtitle": "Свежее зерно, авторские напитки и тёплая атмосфера. Маленькая кофейня с большим сердцем ждёт вас.",
            "cta_text": "Открыть меню",
            "cta_url": "/menu/",
            "is_active": True,
            "order": 0,
        }
        slide, _ = HeroSlide.objects.update_or_create(
            title="Кофе как ритуал.",
            defaults=defaults,
        )
        img = _img_path("hero/hero-main.jpg")
        if img:
            slide.image.name = img
            slide.save()
        self.stdout.write("  -- hero slide ready")

    def _story(self):
        blocks = [
            (
                "Our story",
                "Маленькая кофейня с большим сердцем.",
                "Мы начали с простой идеи — место, в которое хочется возвращаться. "
                "Сегодня Yarcoffee — это команда, которая знает гостей по именам, и зерно, "
                "которое мы обновляем каждую неделю.",
                "story/story-1.jpg",
                0,
            ),
            (
                "Our craft",
                "Кофе — это ремесло.",
                "Мы готовим напитки руками — медленно, внимательно, с уважением к каждому грамму. "
                "Эспрессо, авторские лимонады, домашние десерты — всё с одной целью: чтобы было вкусно.",
                "story/story-2.jpg",
                1,
            ),
            (
                "Community",
                "Место, где день начинается.",
                "С 7:30 утра до 22:45 вечера. Утренний кофе на вынос, обеденная встреча, "
                "вечерний разговор. Здесь хорошо в любое время.",
                "story/story-3.jpg",
                2,
            ),
        ]
        for eyebrow, title, body, img, order in blocks:
            obj, _ = StorySection.objects.update_or_create(
                title=title,
                defaults={"eyebrow": eyebrow, "body": body, "order": order, "is_active": True},
            )
            p = _img_path(img)
            if p:
                obj.image.name = p
                obj.image_alt = title
                obj.save()
        self.stdout.write("  -- story sections ready")

    def _features(self):
        features = [
            ("Specialty зерно", "Свежая обжарка от партнёров, которым мы доверяем.", "beans", 0),
            ("Free Wi-Fi", "Работайте и встречайтесь у нас часами.", "wifi", 1),
            ("Тёплая атмосфера", "Уютный интерьер и дружелюбная команда.", "heart", 2),
            ("07:30 — 22:45", "Открыты каждый день недели.", "clock", 3),
        ]
        for title, desc, icon, order in features:
            Feature.objects.update_or_create(
                title=title,
                defaults={"description": desc, "icon": icon, "order": order, "is_active": True},
            )
        self.stdout.write("  -- features ready")

    def _categories_and_drinks(self):
        categories_data = [
            ("Кофе", "coffee", "Hot coffee", "Эспрессо-основа, классика и наши авторские чашки.", "cup", 0),
            ("Айс-меню", "ice", "Iced & cold", "Холодные напитки на лето и ясные дни.", "ice", 1),
            ("Авторское", "signature", "Signature", "Наши фирменные напитки, которые не повторяет никто.", "cup", 2),
            ("Молочные", "milkshakes", "Milk drinks", "Молочные коктейли и латте на растительном.", "cup", 3),
            ("Не кофе", "not-coffee", "Tea & more", "Матча, лимонады, авторские чаи.", "leaf", 4),
            ("Десерты", "desserts", "Desserts", "Свежая выпечка и десерты к чашке.", "croissant", 5),
        ]
        cats = {}
        for name, slug, eyebrow, desc, icon, order in categories_data:
            cat, _ = DrinkCategory.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "eyebrow": eyebrow,
                    "description": desc,
                    "icon": icon,
                    "order": order,
                    "is_active": True,
                },
            )
            cats[slug] = cat

        drinks_data = [
            ("coffee", "Эспрессо", "Классический выстрел зерна неделя в неделю.",
             14, "30 мл", "крепкий, бодрящий", "drinks/espresso.jpg", False, False, 0),
            ("coffee", "Капучино", "Тёплое молоко, бархатная пенка, мягкий вкус.",
             22, "250 мл", "молочный, мягкий", "drinks/cappuccino.jpg", True, False, 1),
            ("coffee", "Флэт-уайт", "Двойной эспрессо с микропенкой для ценителей.",
             24, "200 мл", "крепкий, кремовый", "drinks/flat-white.jpg", True, False, 2),
            ("coffee", "Мокко", "Эспрессо с шоколадом и взбитыми сливками.",
             28, "300 мл", "сладкий, десертный", "drinks/mocha.jpg", False, False, 3),

            ("ice", "Айс-латте", "Эспрессо со льдом и холодным молоком.",
             26, "350 мл", "айс, освежающий", "drinks/iced-latte.jpg", True, False, 0),
            ("ice", "Колд-брю", "12-часовое холодное заваривание. Тонкий вкус.",
             30, "350 мл", "айс, ягодный", "drinks/cold-brew.jpg", False, True, 1),
            ("ice", "Айс-матча", "Японская матча на холодном молоке.",
             32, "350 мл", "айс, матча", "drinks/matcha.jpg", True, False, 2),

            ("signature", "Raffaello Latte", "Авторский латте с кокосом и миндалём.",
             34, "350 мл", "авторский, сладкий", "drinks/raffaello.jpg", True, True, 0),
            ("signature", "Yar Specialty", "Авторская подача от шеф-бариста.",
             38, "300 мл", "авторский, яркий", "drinks/beans.jpg", True, False, 1),

            ("milkshakes", "Ванильный милкшейк", "Молочный коктейль с натуральной ванилью.",
             28, "400 мл", "сладкий, холодный", "drinks/milkshake.jpg", False, False, 0),
            ("milkshakes", "Клубничный милкшейк", "Свежая клубника и мороженое.",
             30, "400 мл", "ягодный, сладкий", "drinks/milkshake.jpg", False, False, 1),

            ("not-coffee", "Матча латте", "Японская матча на тёплом молоке.",
             30, "300 мл", "матча, мягкий", "drinks/matcha.jpg", False, False, 0),
            ("not-coffee", "Ягодный лимонад", "Домашний лимонад из сезонных ягод.",
             24, "400 мл", "освежающий, ягодный", "drinks/lemonade.jpg", False, False, 1),

            ("desserts", "Круассан", "Слоёный круассан, выпечка дня.",
             18, "1 шт.", "выпечка, свежее", "drinks/croissant.jpg", False, False, 0),
            ("desserts", "Чизкейк", "Нью-Йорк чизкейк с ягодным соусом.",
             28, "150 г", "десерт, сладкий", "drinks/cheesecake.jpg", True, False, 1),
        ]
        for cat_slug, name, short, price, volume, tags, img, feat, new, order in drinks_data:
            cat = cats.get(cat_slug)
            if not cat:
                continue
            drink, _ = Drink.objects.update_or_create(
                name=name,
                category=cat,
                defaults={
                    "short_description": short,
                    "price": Decimal(str(price)),
                    "price_label": "TMT",
                    "volume": volume,
                    "tags": tags,
                    "is_featured": feat,
                    "is_new": new,
                    "is_active": True,
                    "order": order,
                },
            )
            p = _img_path(img)
            if p:
                drink.image.name = p
                drink.save()
        self.stdout.write("  -- categories & drinks ready")

    def _team(self):
        team = [
            ("Шахрух", "Head Barista", "Готовит ваш кофе с 2022 года.", "team/t-1.jpg", 0),
            ("Айгуль", "Barista", "Любит латте-арт и поговорить про музыку.", "team/t-2.jpg", 1),
            ("Мерген", "Barista", "Эксперт по матча и холодным напиткам.", "team/t-3.jpg", 2),
            ("Лейла", "Pastry", "Печёт круассаны и чизкейки каждое утро.", "team/t-4.jpg", 3),
        ]
        for name, role, bio, img, order in team:
            m, _ = TeamMember.objects.update_or_create(
                name=name,
                defaults={"role": role, "bio": bio, "order": order, "is_active": True},
            )
            p = _img_path(img)
            if p:
                m.photo.name = p
                m.save()
        self.stdout.write("  -- team ready")

    def _reviews(self):
        reviews = [
            ("Мария", "Постоянный гость",
             "Лучший айс-латте в городе. Атмосфера простая и тёплая, как дома.", 5),
            ("Артём", "Гость",
             "Зашёл на кофе на вынос — остался на час. Очень хорошо.", 5),
            ("Камилла", "Гость",
             "Очень люблю их Raffaello latte. Стабильно вкусно.", 5),
            ("Денис", "Постоянный гость",
             "Уютно работать днём. Хорошее зерно, дружелюбные ребята.", 5),
            ("Сабина", "Гость",
             "Подача напитков на уровне. Видно, что любят своё дело.", 4),
            ("Игорь", "Гость",
             "Маленькое место с большим характером. Возвращаюсь снова.", 5),
        ]
        for author, role, text, rating in reviews:
            Review.objects.update_or_create(
                author=author,
                text=text,
                defaults={"role": role, "rating": rating, "is_featured": True},
            )
        self.stdout.write("  -- reviews ready")

    def _gallery(self):
        items = [
            ("Утро в кофейне", "moments", "large", "gallery/g-1.jpg", 0),
            ("Латте-арт", "drinks", "normal", "gallery/g-2.jpg", 1),
            ("Барная стойка", "interior", "tall", "gallery/g-3.jpg", 2),
            ("Айс-меню", "drinks", "normal", "gallery/g-4.jpg", 3),
            ("Гости", "people", "normal", "gallery/g-5.jpg", 4),
            ("Зерно", "moments", "wide", "gallery/g-6.jpg", 5),
            ("Эспрессо", "drinks", "normal", "gallery/g-7.jpg", 6),
            ("Свет утра", "interior", "tall", "gallery/g-8.jpg", 7),
            ("Десерты", "drinks", "normal", "gallery/g-9.jpg", 8),
            ("Команда", "people", "wide", "gallery/g-10.jpg", 9),
            ("Атмосфера", "moments", "normal", "gallery/g-11.jpg", 10),
            ("Витрина", "interior", "normal", "gallery/g-12.jpg", 11),
        ]
        for title, cat, span, img, order in items:
            obj, created = GalleryImage.objects.get_or_create(
                title=title,
                defaults={"category": cat, "span": span, "order": order, "is_active": True},
            )
            if not created:
                obj.category = cat
                obj.span = span
                obj.order = order
                obj.is_active = True
            p = _img_path(img)
            if p:
                obj.image.name = p
            obj.save()
        self.stdout.write("  -- gallery ready")

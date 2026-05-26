from django.core.management.base import BaseCommand

from apps.core.i18n import UI_TEXT, localize_text
from apps.core.models import Feature, HeroSlide, Review, SiteSettings, StorySection, TeamMember
from apps.gallery.models import GalleryImage
from apps.menu.models import Drink, DrinkCategory


TRANSLATED_FIELDS = {
    SiteSettings: (
        "brand_name",
        "tagline",
        "address",
        "address_secondary",
        "working_hours",
        "footer_note",
    ),
    HeroSlide: ("eyebrow", "title", "subtitle", "cta_text"),
    StorySection: ("eyebrow", "title", "body", "image_alt"),
    TeamMember: ("name", "role", "bio"),
    Review: ("author", "role", "text"),
    Feature: ("title", "description"),
    DrinkCategory: ("name", "description", "eyebrow"),
    Drink: ("name", "short_description", "description", "tags", "volume", "price_label"),
    GalleryImage: ("title",),
}

SITE_OVERRIDES = {
    "brand_name": {"tk": "Yarcoffee", "ru": "Yarcoffee", "en": "Yarcoffee"},
    "tagline": {
        "tk": UI_TEXT["tk"]["site_tagline"],
        "ru": UI_TEXT["ru"]["site_tagline"],
        "en": UI_TEXT["en"]["site_tagline"],
    },
    "footer_note": {
        "tk": "Söýgi bilen taýýarlanan. Goňşular üçin demlenen.",
        "ru": "Crafted with love. Brewed for the neighbourhood.",
        "en": "Crafted with love. Brewed for the neighbourhood.",
    },
}


class Command(BaseCommand):
    help = "Populate django-modeltranslation fields for TM/RU/EN from existing demo content."

    def handle(self, *args, **options):
        updated = 0
        for model, fields in TRANSLATED_FIELDS.items():
            for obj in model.objects.all():
                for field in fields:
                    source = obj.__dict__.get(field) or getattr(obj, field, "") or ""
                    values = self._values_for(obj, field, source)
                    for lang, value in values.items():
                        setattr(obj, f"{field}_{lang}", value)
                obj.save()
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"[OK] Synced translations for {updated} objects."))

    def _values_for(self, obj, field, source):
        if isinstance(obj, SiteSettings) and field in SITE_OVERRIDES:
            return SITE_OVERRIDES[field]
        return {
            "tk": localize_text(source, "tk"),
            "ru": source,
            "en": localize_text(source, "en"),
        }

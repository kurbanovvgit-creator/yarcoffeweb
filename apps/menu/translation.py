from modeltranslation.translator import TranslationOptions, register

from .models import Drink, DrinkCategory


@register(DrinkCategory)
class DrinkCategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description", "eyebrow")


@register(Drink)
class DrinkTranslationOptions(TranslationOptions):
    fields = ("name", "short_description", "description", "tags", "volume", "price_label")

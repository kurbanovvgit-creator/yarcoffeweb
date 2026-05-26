from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Drink, DrinkCategory


@admin.register(DrinkCategory)
class DrinkCategoryAdmin(TranslationAdmin):
    list_display = ("name", "slug", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Drink)
class DrinkAdmin(TranslationAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "is_featured",
        "is_new",
        "is_active",
        "order",
    )
    list_editable = ("is_featured", "is_new", "is_active", "order")
    list_filter = ("category", "is_featured", "is_new", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description", "tags")
    autocomplete_fields = ("category",)
    fieldsets = (
        (None, {"fields": ("category", "name", "slug", "image")}),
        ("Контент", {"fields": ("short_description", "description", "tags", "volume")}),
        ("Цена", {"fields": ("price", "price_label")}),
        ("Витрина", {"fields": ("is_featured", "is_new", "is_active", "order")}),
    )

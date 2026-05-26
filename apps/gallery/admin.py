from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(TranslationAdmin):
    list_display = ("title", "category", "span", "order", "is_active", "created_at")
    list_editable = ("category", "span", "order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title",)

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
    ContactMessage,
    Feature,
    HeroSlide,
    Review,
    SiteSettings,
    StorySection,
    TeamMember,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(TranslationAdmin):
    fieldsets = (
        ("Бренд", {"fields": ("brand_name", "tagline", "footer_note")}),
        ("Контакты", {"fields": ("phone", "email", "address", "address_secondary", "working_hours")}),
        ("Соцсети", {"fields": ("instagram", "tiktok", "telegram", "whatsapp")}),
        ("Карта", {"fields": ("map_embed_url",)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(TranslationAdmin):
    list_display = ("title", "eyebrow", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle")


@admin.register(StorySection)
class StorySectionAdmin(TranslationAdmin):
    list_display = ("title", "eyebrow", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(TeamMember)
class TeamMemberAdmin(TranslationAdmin):
    list_display = ("name", "role", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "role")


@admin.register(Review)
class ReviewAdmin(TranslationAdmin):
    list_display = ("author", "rating", "is_featured", "created_at")
    list_filter = ("rating", "is_featured")
    list_editable = ("is_featured",)
    search_fields = ("author", "text")


@admin.register(Feature)
class FeatureAdmin(TranslationAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    list_editable = ("is_read",)
    readonly_fields = ("created_at",)
    search_fields = ("name", "email", "phone", "message")

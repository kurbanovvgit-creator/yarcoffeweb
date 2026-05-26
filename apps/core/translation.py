from modeltranslation.translator import TranslationOptions, register

from .models import Feature, HeroSlide, Review, SiteSettings, StorySection, TeamMember


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = (
        "brand_name",
        "tagline",
        "address",
        "address_secondary",
        "working_hours",
        "footer_note",
    )


@register(HeroSlide)
class HeroSlideTranslationOptions(TranslationOptions):
    fields = ("eyebrow", "title", "subtitle", "cta_text")


@register(StorySection)
class StorySectionTranslationOptions(TranslationOptions):
    fields = ("eyebrow", "title", "body", "image_alt")


@register(TeamMember)
class TeamMemberTranslationOptions(TranslationOptions):
    fields = ("name", "role", "bio")


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ("author", "role", "text")


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ("title", "description")

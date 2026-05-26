from django.contrib import messages
from django.shortcuts import redirect, render

from apps.gallery.models import GalleryImage
from apps.menu.models import Drink, DrinkCategory

from .forms import ContactForm
from .i18n import get_ui, normalize_language
from .models import Feature, HeroSlide, Review, StorySection, TeamMember


def home(request, lang=None):
    hero_slides = HeroSlide.objects.filter(is_active=True)
    featured_drinks = Drink.objects.filter(is_featured=True, is_active=True)[:6]
    bean_drinks = Drink.objects.filter(
        is_active=True, category__slug__in=["beans", "zerno"]
    )[:3]
    story_blocks = StorySection.objects.filter(is_active=True)[:2]
    features = Feature.objects.filter(is_active=True)[:4]
    gallery_preview = GalleryImage.objects.filter(is_active=True)[:6]
    reviews = Review.objects.filter(is_featured=True)[:6]
    categories = DrinkCategory.objects.filter(is_active=True)[:6]

    return render(
        request,
        "pages/home.html",
        {
            "hero_slides": hero_slides,
            "featured_drinks": featured_drinks,
            "bean_drinks": bean_drinks,
            "story_blocks": story_blocks,
            "features": features,
            "gallery_preview": gallery_preview,
            "reviews": reviews,
            "categories": categories,
        },
    )


def about(request, lang=None):
    story_blocks = StorySection.objects.filter(is_active=True)
    team = TeamMember.objects.filter(is_active=True)
    features = Feature.objects.filter(is_active=True)
    interior = GalleryImage.objects.filter(is_active=True, category="interior")[:6]
    return render(
        request,
        "pages/about.html",
        {
            "story_blocks": story_blocks,
            "team": team,
            "features": features,
            "interior": interior,
        },
    )


def contacts(request, lang=None):
    active_lang = normalize_language(lang)
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, get_ui(active_lang)["contact_success"])
            return redirect("/contacts/" if active_lang == "tk" else f"/{active_lang}/contacts/")
    else:
        form = ContactForm()
    return render(request, "pages/contacts.html", {"form": form})

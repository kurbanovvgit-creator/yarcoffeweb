from django.shortcuts import render

from .models import CATEGORY_CHOICES, GalleryImage


def gallery_list(request, lang=None):
    category = request.GET.get("category")
    images = GalleryImage.objects.filter(is_active=True)
    if category:
        images = images.filter(category=category)
    return render(
        request,
        "pages/gallery.html",
        {
            "images": images,
            "categories": CATEGORY_CHOICES,
            "active_category": category,
        },
    )

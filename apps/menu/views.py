from django.shortcuts import render

from .models import Drink, DrinkCategory


def menu_list(request, lang=None):
    categories = DrinkCategory.objects.filter(is_active=True).prefetch_related("drinks")
    active_category = request.GET.get("category")
    return render(
        request,
        "pages/menu.html",
        {
            "categories": categories,
            "active_category": active_category,
        },
    )

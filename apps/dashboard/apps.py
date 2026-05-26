import json

from django.apps import AppConfig
from django.contrib import admin


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"
    verbose_name = "Yarcoffee · Dashboard"

    def ready(self):
        admin.site.site_header = "YARCOFFEE · ADMIN"
        admin.site.site_title = "Yarcoffee · Admin"
        admin.site.index_title = "Панель управления"

        # Inject dashboard stats into the admin context so the custom
        # index template can render quick KPI cards.
        original_each_context = admin.site.each_context

        def each_context_with_stats(request):
            context = original_each_context(request)
            context["yc_stats_json"] = json.dumps(_collect_stats())
            return context

        admin.site.each_context = each_context_with_stats


def _collect_stats():
    try:
        from apps.core.models import ContactMessage, Review, TeamMember
        from apps.gallery.models import GalleryImage
        from apps.menu.models import Drink, DrinkCategory

        return {
            "drinks": Drink.objects.count(),
            "categories": DrinkCategory.objects.count(),
            "gallery": GalleryImage.objects.count(),
            "reviews": Review.objects.count(),
            "messages": ContactMessage.objects.count(),
            "team": TeamMember.objects.count(),
        }
    except Exception:
        return {}

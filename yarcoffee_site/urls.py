"""URL configuration for the Yarcoffee site."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from apps.core import views as core_views
from apps.gallery import views as gallery_views
from apps.menu import views as menu_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("menu/", include("apps.menu.urls")),
    path("gallery/", include("apps.gallery.urls")),
    re_path(r"^(?P<lang>tk|ru|en)/$", core_views.home),
    re_path(r"^(?P<lang>tk|ru|en)/about/$", core_views.about),
    re_path(r"^(?P<lang>tk|ru|en)/contacts/$", core_views.contacts),
    re_path(r"^(?P<lang>tk|ru|en)/menu/$", menu_views.menu_list),
    re_path(r"^(?P<lang>tk|ru|en)/gallery/$", gallery_views.gallery_list),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

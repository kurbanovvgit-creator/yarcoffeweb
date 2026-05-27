"""Resolve image URLs for admin uploads (media/) and seeded static files (static/images/)."""

from django.conf import settings
from django.templatetags.static import static


def resolve_asset_url(file_field) -> str:
    """Return a public URL for an ImageField/FileField value."""
    if not file_field:
        return ""
    name = (file_field.name or "").strip()
    if not name:
        return ""

    media_path = settings.MEDIA_ROOT / name
    if media_path.is_file():
        return file_field.url

    static_dirs = getattr(settings, "STATICFILES_DIRS", [])
    if static_dirs:
        static_path = static_dirs[0] / "images" / name
        if static_path.is_file():
            return static(f"images/{name}")

    return file_field.url

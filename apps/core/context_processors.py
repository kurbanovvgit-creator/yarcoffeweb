"""Inject global site context into every template."""

from .models import SiteSettings
from .i18n import DEFAULT_LANGUAGE, LANGUAGE_OPTIONS, get_ui, normalize_language


def _current_language(request):
    match = getattr(request, "resolver_match", None)
    kwargs = getattr(match, "kwargs", {}) if match else {}
    return normalize_language(kwargs.get("lang", DEFAULT_LANGUAGE))


def _localized_url(path, lang):
    parts = [part for part in path.split("/") if part]
    if parts and parts[0] in {"tk", "ru", "en"}:
        parts = parts[1:]
    clean_path = "/" + "/".join(parts) + ("/" if parts else "")
    if lang == DEFAULT_LANGUAGE:
        return clean_path
    return f"/{lang}{clean_path}"


def _site_urls(lang):
    prefix = "" if lang == DEFAULT_LANGUAGE else f"/{lang}"
    return {
        "home": f"{prefix}/",
        "menu": f"{prefix}/menu/",
        "about": f"{prefix}/about/",
        "contacts": f"{prefix}/contacts/",
        "gallery": f"{prefix}/gallery/",
    }


def site_context(request):
    settings_obj = SiteSettings.get_solo()
    lang = _current_language(request)
    language_options = [
        {
            **option,
            "active": option["code"] == lang,
            "url": _localized_url(request.path, option["code"]),
        }
        for option in LANGUAGE_OPTIONS
    ]
    return {
        "site_settings": settings_obj,
        "year": __import__("datetime").datetime.now().year,
        "current_language": lang,
        "language_options": language_options,
        "site_urls": _site_urls(lang),
        "tr": get_ui(lang),
    }

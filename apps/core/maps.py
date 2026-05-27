"""Google Maps URLs for embed and external links."""

from urllib.parse import quote_plus

# Official embed from Google Maps → Share → Embed (ÝARcoffee, Ashgabat)
DEFAULT_MAP_EMBED_URL = (
    "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d26888.893790685728!"
    "2d58.35219072492952!3d37.90780940000001!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!"
    "3m3!1m2!1s0x3f6ffd00329d28e1%3A0x6f327a51b8e8efd0!2s%C3%9DARcoffee!5e1!3m2!1sru!2sus!"
    "4v1779867304819!5m2!1sru!2sus"
)

DEFAULT_MAP_OPEN_URL = (
    "https://www.google.com/maps/place/%C3%9DARcoffee/"
    "@37.9078094,58.3547656,17z/data=!3m1!4b1!4m6!3m5!1s0x3f6ffd00329d28e1:0x6f327a51b8e8efd0!"
    "8m2!3d37.9078094!4d58.3547656!16s%2Fg%2F11y3v8qvxq?entry=ttu"
)


def _looks_like_hours(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in ("07:", "22:", "07:30", "каждый день", "every day", "·"))


def map_search_query(settings) -> str:
    parts = []
    if settings.brand_name:
        parts.append(settings.brand_name.strip())
    if settings.address:
        parts.append(settings.address.strip())
    if settings.address_secondary and not _looks_like_hours(settings.address_secondary):
        parts.append(settings.address_secondary.strip())
    joined = ", ".join(p for p in parts if p)
    lowered = joined.lower()
    if "ашхабад" not in lowered and "ashgabat" not in lowered:
        joined = f"{joined}, Ashgabat" if joined else "Ashgabat"
    if "туркмен" not in lowered and "turkmen" not in lowered:
        joined = f"{joined}, Turkmenistan"
    return joined or "Yarcoffee, Ashgabat, Turkmenistan"


def map_open_url(settings) -> str:
    custom = (settings.map_embed_url or "").strip()
    if custom and "google.com/maps/embed" in custom:
        return DEFAULT_MAP_OPEN_URL
    return f"https://www.google.com/maps/search/?api=1&query={quote_plus(map_search_query(settings))}"


def map_iframe_src(settings) -> str:
    custom = (settings.map_embed_url or "").strip()
    if custom and "openstreetmap" not in custom:
        return custom
    return DEFAULT_MAP_EMBED_URL

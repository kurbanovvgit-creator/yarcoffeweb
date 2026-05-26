from django import template

from apps.core.i18n import localize_text

register = template.Library()


@register.filter
def lt(value, lang):
    """Localize known seeded/demo content."""
    return localize_text(value, lang)

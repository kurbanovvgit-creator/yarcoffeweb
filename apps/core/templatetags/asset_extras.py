from django import template

from apps.core.assets import resolve_asset_url

register = template.Library()


@register.filter
def asset_url(file_field):
    """Media upload URL, or static/images/ fallback for seeded demo files."""
    return resolve_asset_url(file_field)

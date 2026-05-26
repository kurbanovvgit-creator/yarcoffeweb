from django.utils import translation

from .i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, normalize_language


class LanguagePrefixMiddleware:
    """Activate language from /ru/ and /en/ URL prefixes.

    URLs without a language prefix are treated as the default Turkmen version.
    This also lets django-modeltranslation resolve translated fields correctly
    outside of the manual UI translation dictionary.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        first_part = request.path_info.strip("/").split("/", 1)[0]
        language = normalize_language(
            first_part if first_part in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
        )
        translation.activate(language)
        request.LANGUAGE_CODE = language
        try:
            return self.get_response(request)
        finally:
            translation.deactivate()

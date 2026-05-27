"""Core models — site settings, hero content, story, team, reviews, contact submissions."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from .maps import DEFAULT_MAP_EMBED_URL


class SiteSettings(models.Model):
    """Singleton-style model holding global site settings."""

    brand_name = models.CharField(_("Название бренда"), max_length=120, default="Yarcoffee")
    tagline = models.CharField(
        _("Слоган"),
        max_length=255,
        default="Маленькая кофейня с большим сердцем",
    )
    phone = models.CharField(_("Телефон"), max_length=64, default="+993 65 722525")
    email = models.EmailField(_("E-mail"), default="hello@yarcoffee.tm")
    address = models.CharField(_("Адрес"), max_length=255, default="Ашхабад, ул. Туркменбаши")
    address_secondary = models.CharField(
        _("Адрес (доп.)"), max_length=255, blank=True, default=""
    )
    working_hours = models.CharField(
        _("Часы работы"), max_length=120, default="Каждый день · 07:30 — 22:45"
    )
    instagram = models.URLField(_("Instagram"), default="https://www.instagram.com/yarcoffee.tm/")
    tiktok = models.URLField(_("TikTok"), default="https://www.tiktok.com/@yarcoffee.tm")
    telegram = models.URLField(_("Telegram"), blank=True, default="")
    whatsapp = models.URLField(_("WhatsApp"), blank=True, default="")
    map_embed_url = models.URLField(
        _("Карта (embed URL)"),
        max_length=500,
        blank=True,
        default=DEFAULT_MAP_EMBED_URL,
        help_text=_("Embed-ссылка из Google Maps → Поделиться → Встроить карту."),
    )

    footer_note = models.TextField(
        _("Подпись в футере"),
        default="Crafted with love. Brewed for the neighbourhood.",
    )

    class Meta:
        verbose_name = _("Настройки сайта")
        verbose_name_plural = _("Настройки сайта")

    def __str__(self):
        return self.brand_name

    @classmethod
    def get_solo(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj

    def map_search_query(self):
        from .maps import map_search_query

        return map_search_query(self)

    @property
    def map_open_url(self):
        from .maps import map_open_url

        return map_open_url(self)

    @property
    def map_iframe_src(self):
        from .maps import map_iframe_src

        return map_iframe_src(self)


class HeroSlide(models.Model):
    """Fullscreen hero slides for the homepage."""

    eyebrow = models.CharField(_("Надпись сверху"), max_length=80, default="Specialty coffee")
    title = models.CharField(_("Заголовок"), max_length=200)
    subtitle = models.CharField(_("Подзаголовок"), max_length=255, blank=True, default="")
    cta_text = models.CharField(_("Текст ссылки"), max_length=60, blank=True, default="Смотреть меню")
    cta_url = models.CharField(_("Ссылка"), max_length=200, blank=True, default="/menu/")
    image = models.ImageField(_("Фон"), upload_to="hero/", blank=True, null=True)
    is_active = models.BooleanField(_("Показывать"), default=True)
    order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Hero · слайд")
        verbose_name_plural = _("Hero · слайды")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class StorySection(models.Model):
    """The 'about / brand story' content blocks."""

    eyebrow = models.CharField(_("Надпись сверху"), max_length=80, default="Our story")
    title = models.CharField(_("Заголовок"), max_length=200, default="Маленькая кофейня с большим сердцем")
    body = models.TextField(_("Текст"))
    image = models.ImageField(_("Изображение"), upload_to="story/", blank=True, null=True)
    image_alt = models.CharField(_("Alt"), max_length=200, blank=True, default="")
    order = models.PositiveIntegerField(_("Порядок"), default=0)
    is_active = models.BooleanField(_("Показывать"), default=True)

    class Meta:
        verbose_name = _("История · блок")
        verbose_name_plural = _("История · блоки")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    """A barista or staff member shown on the About page."""

    name = models.CharField(_("Имя"), max_length=120)
    role = models.CharField(_("Должность"), max_length=120, default="Barista")
    bio = models.TextField(_("О себе"), blank=True, default="")
    photo = models.ImageField(_("Фото"), upload_to="team/", blank=True, null=True)
    order = models.PositiveIntegerField(_("Порядок"), default=0)
    is_active = models.BooleanField(_("Показывать"), default=True)

    class Meta:
        verbose_name = _("Команда · участник")
        verbose_name_plural = _("Команда")
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name} · {self.role}"


class Review(models.Model):
    """Guest reviews displayed in the testimonials section."""

    author = models.CharField(_("Автор"), max_length=120)
    role = models.CharField(_("Подпись"), max_length=160, blank=True, default="Гость")
    text = models.TextField(_("Отзыв"))
    rating = models.PositiveSmallIntegerField(
        _("Оценка"),
        default=5,
        choices=[(i, "★" * i) for i in range(1, 6)],
    )
    avatar = models.ImageField(_("Аватар"), upload_to="reviews/", blank=True, null=True)
    is_featured = models.BooleanField(_("Отображать"), default=True)
    created_at = models.DateTimeField(_("Дата"), auto_now_add=True)

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author} · {self.rating}★"


class Feature(models.Model):
    """Small marketing features (Wi-Fi, free refill, etc.) shown on the homepage."""

    title = models.CharField(_("Заголовок"), max_length=120)
    description = models.CharField(_("Описание"), max_length=240, blank=True, default="")
    icon = models.CharField(
        _("Иконка"),
        max_length=40,
        default="cup",
        help_text="cup, wifi, leaf, clock, heart, beans",
    )
    order = models.PositiveIntegerField(_("Порядок"), default=0)
    is_active = models.BooleanField(_("Показывать"), default=True)

    class Meta:
        verbose_name = _("Преимущество")
        verbose_name_plural = _("Преимущества")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Submissions from the contact form."""

    name = models.CharField(_("Имя"), max_length=120)
    email = models.EmailField(_("E-mail"), blank=True, default="")
    phone = models.CharField(_("Телефон"), max_length=40, blank=True, default="")
    message = models.TextField(_("Сообщение"))
    created_at = models.DateTimeField(_("Получено"), auto_now_add=True)
    is_read = models.BooleanField(_("Прочитано"), default=False)

    class Meta:
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} · {self.created_at:%d.%m.%Y %H:%M}"

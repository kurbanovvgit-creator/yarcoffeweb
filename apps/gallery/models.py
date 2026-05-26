"""Gallery models — masonry images grouped by category."""

from django.db import models
from django.utils.translation import gettext_lazy as _


CATEGORY_CHOICES = [
    ("drinks", "Напитки"),
    ("interior", "Интерьер"),
    ("people", "Люди"),
    ("moments", "Моменты"),
]


class GalleryImage(models.Model):
    title = models.CharField(_("Подпись"), max_length=160, blank=True, default="")
    category = models.CharField(
        _("Категория"),
        max_length=32,
        choices=CATEGORY_CHOICES,
        default="moments",
    )
    image = models.ImageField(_("Изображение"), upload_to="gallery/", blank=True, null=True)
    span = models.CharField(
        _("Размер плитки"),
        max_length=20,
        choices=[
            ("normal", "1×1"),
            ("tall", "1×2"),
            ("wide", "2×1"),
            ("large", "2×2"),
        ],
        default="normal",
    )
    order = models.PositiveIntegerField(_("Порядок"), default=0)
    is_active = models.BooleanField(_("Показывать"), default=True)
    created_at = models.DateTimeField(_("Добавлено"), auto_now_add=True)

    class Meta:
        verbose_name = _("Галерея · изображение")
        verbose_name_plural = _("Галерея")
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title or f"Изображение #{self.pk}"

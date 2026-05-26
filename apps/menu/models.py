"""Menu models — drink categories and individual drinks."""

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class DrinkCategory(models.Model):
    name = models.CharField(_("Название"), max_length=80)
    slug = models.SlugField(_("Slug"), max_length=80, unique=True, blank=True)
    description = models.CharField(_("Описание"), max_length=255, blank=True, default="")
    eyebrow = models.CharField(
        _("Надпись"), max_length=80, blank=True, default="Signature category"
    )
    icon = models.CharField(
        _("Иконка"),
        max_length=40,
        default="cup",
        help_text="cup, beans, leaf, snow, croissant, ice",
    )
    order = models.PositiveIntegerField(_("Порядок"), default=0)
    is_active = models.BooleanField(_("Показывать"), default=True)

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ["order", "id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) or "category"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Drink(models.Model):
    category = models.ForeignKey(
        DrinkCategory,
        on_delete=models.CASCADE,
        related_name="drinks",
        verbose_name=_("Категория"),
    )
    name = models.CharField(_("Название"), max_length=120)
    slug = models.SlugField(_("Slug"), max_length=140, unique=True, blank=True)
    short_description = models.CharField(_("Короткое описание"), max_length=255, blank=True, default="")
    description = models.TextField(_("Описание"), blank=True, default="")
    price = models.DecimalField(_("Цена"), max_digits=8, decimal_places=2, default=0)
    price_label = models.CharField(
        _("Подпись к цене"),
        max_length=20,
        blank=True,
        default="TMT",
        help_text="Валюта/единица — выводится рядом с числом",
    )
    volume = models.CharField(_("Объём / порция"), max_length=40, blank=True, default="")
    tags = models.CharField(
        _("Теги"),
        max_length=200,
        blank=True,
        default="",
        help_text="Через запятую: айс, ягодный, авторский",
    )
    image = models.ImageField(_("Изображение"), upload_to="drinks/", blank=True, null=True)
    is_featured = models.BooleanField(_("На главной"), default=False)
    is_new = models.BooleanField(_("Новинка"), default=False)
    is_active = models.BooleanField(_("Показывать"), default=True)
    order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Напиток")
        verbose_name_plural = _("Напитки")
        ordering = ["category__order", "order", "id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "drink"
            slug = base
            counter = 2
            while Drink.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]

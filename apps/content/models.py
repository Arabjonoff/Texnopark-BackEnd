from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import Icon, PublishableModel, Theme, TimeStampedModel


class SiteSettings(TimeStampedModel):
    """Sayt bo'ylab ishlatiladigan aloqa ma'lumotlari (bitta yozuv)."""

    phone = models.CharField('telefon', max_length=50)
    email = models.EmailField('elektron pochta')
    address = models.CharField('manzil', max_length=255)
    working_hours = models.CharField('ish vaqti', max_length=100, blank=True)
    map_url = models.URLField('xarita havolasi', blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    telegram_url = models.URLField('Telegram', blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    youtube_url = models.URLField('YouTube', blank=True)

    class Meta:
        verbose_name = 'sayt sozlamalari'
        verbose_name_plural = 'sayt sozlamalari'

    def __str__(self):
        return 'Sayt sozlamalari'

    def clean(self):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("Sayt sozlamalari faqat bitta bo'lishi mumkin — mavjudini tahrirlang.")

    @classmethod
    def load(cls):
        return cls.objects.first()


class Statistic(PublishableModel):
    value = models.PositiveIntegerField('qiymat')
    suffix = models.CharField("qo'shimcha belgi", max_length=10, blank=True, default='+')
    label = models.CharField('matn', max_length=100)

    class Meta(PublishableModel.Meta):
        verbose_name = 'statistika'
        verbose_name_plural = 'statistika'

    def __str__(self):
        return f'{self.value}{self.suffix} {self.label}'


class Feature(PublishableModel):
    """"Nega aynan biz?" bo'limi kartalari."""

    title = models.CharField('sarlavha', max_length=100)
    description = models.TextField('tavsif')
    icon = models.CharField('ikonka', max_length=30, choices=Icon.choices, default=Icon.ZAP)
    theme = models.CharField('rang', max_length=20, choices=Theme.choices, default=Theme.BLUE)

    class Meta(PublishableModel.Meta):
        verbose_name = 'afzallik'
        verbose_name_plural = "afzalliklar (Nega aynan biz?)"

    def __str__(self):
        return self.title


class Equipment(PublishableModel):
    """Laboratoriya bo'limi."""

    title = models.CharField('nomi', max_length=100)
    description = models.TextField('tavsif')
    icon = models.CharField('ikonka', max_length=30, choices=Icon.choices, default=Icon.CPU)
    theme = models.CharField('rang', max_length=20, choices=Theme.choices, default=Theme.BLUE)
    image = models.ImageField('rasm', upload_to='equipment/', blank=True)

    class Meta(PublishableModel.Meta):
        verbose_name = 'laboratoriya jihozi'
        verbose_name_plural = 'laboratoriya jihozlari'

    def __str__(self):
        return self.title


class Partner(PublishableModel):
    name = models.CharField('nomi', max_length=150)
    logo = models.ImageField('logotip', upload_to='partners/', blank=True)
    url = models.URLField('sayt havolasi', blank=True)

    class Meta(PublishableModel.Meta):
        verbose_name = 'hamkor'
        verbose_name_plural = 'hamkorlar'

    def __str__(self):
        return self.name

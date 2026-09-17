from django.db import models

from apps.core.models import PublishableModel, Theme


class Event(PublishableModel):
    class Status(models.TextChoices):
        UPCOMING = 'upcoming', 'Tez orada'
        OPEN = 'open', "Ro'yxatdan o'tish ochiq"
        CLOSED = 'closed', "Ro'yxatdan o'tish yopilgan"

    slug = models.SlugField('slug (URL)', max_length=150, unique=True)
    title = models.CharField('nomi', max_length=200)
    category = models.CharField('toifa', max_length=50)
    date = models.DateField('sana')
    start_time = models.TimeField('boshlanish vaqti')
    end_time = models.TimeField('tugash vaqti', null=True, blank=True)
    location = models.CharField('manzil', max_length=255)
    short_desc = models.CharField('qisqa tavsif', max_length=300)
    description = models.TextField("to'liq tavsif")
    theme = models.CharField('rang', max_length=20, choices=Theme.choices, default=Theme.BLUE)
    prizes = models.JSONField('sovrinlar', default=list, blank=True)
    requirements = models.JSONField('ishtirok shartlari', default=list, blank=True)
    organizer = models.CharField('tashkilotchi', max_length=200)
    seats = models.PositiveIntegerField("o'rinlar soni")
    status = models.CharField('holati', max_length=20, choices=Status.choices, default=Status.UPCOMING)

    class Meta(PublishableModel.Meta):
        ordering = ('date', 'start_time')
        verbose_name = 'tadbir'
        verbose_name_plural = 'tadbirlar'

    def __str__(self):
        return self.title


class ScheduleItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedule', verbose_name='tadbir')
    time = models.TimeField('vaqt')
    activity = models.CharField('faoliyat', max_length=255)

    class Meta:
        ordering = ('time', 'id')
        verbose_name = 'dastur bandi'
        verbose_name_plural = 'tadbir dasturi'

    def __str__(self):
        return f'{self.time:%H:%M} {self.activity}'

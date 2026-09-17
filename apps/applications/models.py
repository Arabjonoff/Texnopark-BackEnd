from django.db import models

from apps.core.models import TimeStampedModel


class Application(TimeStampedModel):
    """Saytdagi formalardan kelgan murojaatlar: kursga yozilish, tadbirga ro'yxat, umumiy xabar."""

    class Type(models.TextChoices):
        CONTACT = 'contact', 'Umumiy xabar'
        COURSE = 'course', 'Kursga yozilish'
        EVENT = 'event', "Tadbirga ro'yxatdan o'tish"

    class Status(models.TextChoices):
        NEW = 'new', 'Yangi'
        IN_PROGRESS = 'in_progress', "Ko'rib chiqilmoqda"
        DONE = 'done', 'Yakunlangan'
        REJECTED = 'rejected', 'Rad etilgan'

    type = models.CharField('turi', max_length=20, choices=Type.choices, default=Type.CONTACT)
    name = models.CharField('ism', max_length=100)
    phone = models.CharField('telefon', max_length=30)
    message = models.TextField('xabar', blank=True)
    course = models.ForeignKey(
        'courses.Course', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='applications', verbose_name='kurs',
    )
    event = models.ForeignKey(
        'events.Event', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='applications', verbose_name='tadbir',
    )
    status = models.CharField('holati', max_length=20, choices=Status.choices, default=Status.NEW)
    admin_note = models.TextField('admin izohi', blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'murojaat'
        verbose_name_plural = 'murojaatlar'

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'

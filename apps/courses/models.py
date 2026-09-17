from django.db import models

from apps.core.models import Icon, PublishableModel, Theme


class Course(PublishableModel):
    slug = models.SlugField('slug (URL)', max_length=100, unique=True)
    title = models.CharField('nomi', max_length=150)
    short_desc = models.CharField('qisqa tavsif', max_length=300)
    description = models.TextField("to'liq tavsif")
    icon = models.CharField('ikonka', max_length=30, choices=Icon.choices, default=Icon.TERMINAL)
    theme = models.CharField('rang', max_length=20, choices=Theme.choices, default=Theme.BLUE)
    duration = models.CharField('davomiyligi', max_length=50)
    level = models.CharField('daraja', max_length=100)
    format = models.CharField('format', max_length=100)
    price = models.CharField('narxi', max_length=50)
    seats = models.PositiveIntegerField("o'rinlar soni")
    skills = models.JSONField('texnologiyalar', default=list, blank=True)
    outcomes = models.JSONField('kurs natijalari', default=list, blank=True)

    class Meta(PublishableModel.Meta):
        verbose_name = 'kurs'
        verbose_name_plural = 'kurslar'

    def __str__(self):
        return self.title


class CurriculumItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='curriculum', verbose_name='kurs')
    week = models.CharField('hafta', max_length=50)
    topic = models.CharField('mavzu', max_length=255)
    order = models.PositiveIntegerField('tartib', default=0)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = "o'quv dasturi bandi"
        verbose_name_plural = "o'quv dasturi"

    def __str__(self):
        return f'{self.week}: {self.topic}'

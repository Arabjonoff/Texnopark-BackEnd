from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel


class Post(TimeStampedModel):
    slug = models.SlugField('slug (URL)', max_length=150, unique=True)
    title = models.CharField('sarlavha', max_length=200)
    category = models.CharField('toifa', max_length=50)
    excerpt = models.CharField('qisqa matn', max_length=300)
    content = models.TextField("to'liq matn", help_text="Paragraflar bo'sh qator bilan ajratiladi")
    cover = models.ImageField('muqova rasmi', upload_to='news/', blank=True)
    is_published = models.BooleanField("saytda ko'rsatilsin", default=True)
    published_at = models.DateTimeField('chop etilgan vaqt', default=timezone.now)

    class Meta:
        ordering = ('-published_at',)
        verbose_name = 'yangilik'
        verbose_name_plural = 'yangiliklar'

    def __str__(self):
        return self.title

from django.db import models

from apps.core.models import PublishableModel, Theme


class VideoStory(PublishableModel):
    """"O'quvchilar natijalari" — video story kartalari."""

    student_name = models.CharField("o'quvchi ismi", max_length=100)
    course = models.ForeignKey(
        'courses.Course', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='video_stories', verbose_name='kurs',
    )
    course_name = models.CharField(
        'kurs nomi (matn)', max_length=100, blank=True,
        help_text="Kurs tanlanmagan bo'lsa shu matn ko'rsatiladi",
    )
    result = models.CharField('natija', max_length=255)
    video_url = models.URLField('video havolasi', blank=True, help_text='YouTube, Instagram yoki boshqa havola')
    thumbnail = models.ImageField('muqova rasmi', upload_to='stories/', blank=True)
    theme = models.CharField('rang', max_length=20, choices=Theme.choices, default=Theme.BLUE)

    class Meta(PublishableModel.Meta):
        verbose_name = 'video story'
        verbose_name_plural = "o'quvchilar natijalari (video)"

    def __str__(self):
        return f'{self.student_name} — {self.result}'

    @property
    def course_label(self):
        return self.course.title if self.course else self.course_name

"""
Saytning boshlang'ich kontentini (frontend mock data'sidan olingan) bazaga yuklaydi.

    python manage.py seed_data          # mavjud yozuvlarni slug bo'yicha yangilaydi
    python manage.py seed_data --reset  # avval seed qiladigan barcha kontentni o'chiradi (murojaatlar tegilmaydi)
"""

import json
import re
from datetime import date, time
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.content.models import Equipment, Feature, Partner, SiteSettings, Statistic
from apps.core.formatting import UZ_MONTHS
from apps.courses.models import Course, CurriculumItem
from apps.events.models import Event, ScheduleItem
from apps.news.models import Post
from apps.projects.models import VideoStory

SEED_FILE = Path(__file__).resolve().parents[2] / 'seed' / 'initial_data.json'


def theme_from_class(color_class):
    """'bg-blue-500' -> 'blue'"""
    return color_class.split('-')[1]


def parse_uz_date(value):
    """'12 Oktabr, 2026' -> date(2026, 10, 12)"""
    day, month, year = re.match(r'(\d+)\s+(\S+),\s*(\d{4})', value).groups()
    return date(int(year), UZ_MONTHS.index(month) + 1, int(day))


def parse_time(value):
    hours, minutes = value.strip().split(':')
    return time(int(hours), int(minutes))


class Command(BaseCommand):
    help = "Boshlang'ich kontentni (kurslar, tadbirlar, yangiliklar, sayt bo'limlari) bazaga yuklaydi"

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help="Avval mavjud kontentni o'chiradi")

    @transaction.atomic
    def handle(self, *args, reset=False, **options):
        data = json.loads(SEED_FILE.read_text(encoding='utf-8'))

        if reset:
            for model in (VideoStory, Course, Event, Post, Statistic, Feature, Equipment, Partner):
                model.objects.all().delete()

        for order, item in enumerate(data['courses']):
            course, _ = Course.objects.update_or_create(
                slug=item['id'],
                defaults={
                    'title': item['title'],
                    'short_desc': item['shortDesc'],
                    'description': item['description'],
                    'icon': item['icon'],
                    'theme': theme_from_class(item['color']),
                    'duration': item['duration'],
                    'level': item['level'],
                    'format': item['format'],
                    'price': item['price'],
                    'seats': item['seats'],
                    'skills': item['skills'],
                    'outcomes': item['outcomes'],
                    'order': order,
                },
            )
            course.curriculum.all().delete()
            CurriculumItem.objects.bulk_create(
                CurriculumItem(course=course, week=row['week'], topic=row['topic'], order=i)
                for i, row in enumerate(item['curriculum'])
            )

        for order, item in enumerate(data['events']):
            start, _, end = item['time'].partition('—')
            event, _ = Event.objects.update_or_create(
                slug=item['id'],
                defaults={
                    'title': item['title'],
                    'category': item['category'],
                    'date': parse_uz_date(item['date']),
                    'start_time': parse_time(start),
                    'end_time': parse_time(end) if end.strip() else None,
                    'location': item['location'],
                    'short_desc': item['shortDesc'],
                    'description': item['description'],
                    'theme': theme_from_class(item['color']),
                    'prizes': item['prizes'],
                    'requirements': item['requirements'],
                    'organizer': item['organizer'],
                    'seats': item['seats'],
                    'status': item['status'],
                    'order': order,
                },
            )
            event.schedule.all().delete()
            ScheduleItem.objects.bulk_create(
                ScheduleItem(event=event, time=parse_time(row['time']), activity=row['activity'])
                for row in item['schedule']
            )

        self.seed_site_content(data)

        self.stdout.write(self.style.SUCCESS(
            f"Yuklandi: {len(data['courses'])} ta kurs, {len(data['events'])} ta tadbir, "
            f"{len(data['news'])} ta yangilik, {len(data['videoStories'])} ta video story, "
            f"{len(data['partners'])} ta hamkor"
        ))

    def seed_site_content(self, data):
        # Sayt sozlamalari admin'da tahrirlangan bo'lishi mumkin — faqat yo'q bo'lsa yaratiladi
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(**data['siteSettings'])

        # Kalit maydoni yo'q bo'limlar nom bo'yicha yangilanadi
        simple_sections = (
            (Statistic, 'label', data['statistics']),
            (Feature, 'title', data['features']),
            (Equipment, 'title', data['equipment']),
            (Partner, 'name', data['partners']),
        )
        for model, key, rows in simple_sections:
            for order, row in enumerate(rows):
                fields = {**row, 'order': order}
                model.objects.update_or_create(**{key: fields.pop(key)}, defaults=fields)

        for order, row in enumerate(data['videoStories']):
            VideoStory.objects.update_or_create(
                student_name=row['studentName'],
                defaults={
                    'course': Course.objects.filter(slug=row['course']).first(),
                    'result': row['result'],
                    'theme': row['theme'],
                    'order': order,
                },
            )

        for row in data['news']:
            Post.objects.get_or_create(
                slug=row['id'],
                defaults={key: row[key] for key in ('title', 'category', 'excerpt', 'content')},
            )

from datetime import timedelta
from io import StringIO

from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.content.models import Partner, TeamMember
from apps.courses.models import Course
from apps.events.models import Event
from apps.news.models import Post


class SeededApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_data', stdout=StringIO())

    def test_seed_is_idempotent(self):
        call_command('seed_data', stdout=StringIO())
        self.assertEqual(Course.objects.count(), 5)
        self.assertEqual(Event.objects.count(), 3)

    def test_course_list_uses_camel_case_and_slug_id(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, 200)
        first = response.json()[0]
        self.assertEqual(first['id'], 'flutter')
        self.assertIn('shortDesc', first)
        self.assertEqual(first['icon'], 'smartphone')
        self.assertEqual(first['theme'], 'blue')

    def test_course_detail(self):
        response = self.client.get('/api/courses/python/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['curriculum'])
        self.assertEqual(set(data['curriculum'][0]), {'week', 'topic'})
        self.assertTrue(data['skills'])

    def test_unpublished_course_is_hidden(self):
        Course.objects.filter(slug='python').update(is_published=False)
        self.assertEqual(self.client.get('/api/courses/python/').status_code, 404)

    def test_event_detail_matches_frontend_format(self):
        response = self.client.get('/api/events/andijon-ideathon-2026/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['date'], '12 Oktabr, 2026')
        self.assertEqual(data['dateIso'], '2026-10-12')
        self.assertEqual(data['time'], '09:00 — 18:00')
        self.assertEqual(data['schedule'][0], {'time': '09:00', 'activity': "Ro'yxatdan o'tish va ochilish marosimi"})

    def test_event_status_filter(self):
        response = self.client.get('/api/events/?status=upcoming')
        self.assertEqual([e['id'] for e in response.json()], ['robotics-challenge'])

    def test_api_is_read_only(self):
        self.assertEqual(self.client.post('/api/courses/', {}).status_code, 405)

    def test_site_settings(self):
        data = self.client.get('/api/site-settings/').json()
        self.assertEqual(data['phone'], '+998 94 893 00 17')
        self.assertIn('instagramUrl', data)

    def test_content_lists(self):
        self.assertEqual(len(self.client.get('/api/statistics/').json()), 3)
        features = self.client.get('/api/features/').json()
        self.assertEqual([f['icon'] for f in features], ['briefcase', 'rocket', 'zap', 'users', 'trophy'])
        self.assertEqual(len(self.client.get('/api/equipment/').json()), 4)
        self.assertEqual(self.client.get('/api/partners/').json()[0], {'id': Partner.objects.get(name='IT Park').id, 'name': 'IT Park', 'logo': None, 'url': ''})

    def test_video_story_course_label(self):
        story = self.client.get('/api/video-stories/').json()[0]
        self.assertEqual(story['course'], 'Flutter Development')
        self.assertEqual(story['courseSlug'], 'flutter')

    def test_news_hides_future_posts(self):
        Post.objects.create(
            slug='kelajak', title='Kelajak', category='E\'lon', excerpt='x', content='x',
            published_at=timezone.now() + timedelta(days=1),
        )
        slugs = [p['id'] for p in self.client.get('/api/news/').json()]
        self.assertEqual(slugs, ['yangi-oquv-mavsumi-qabul'])
        self.assertEqual(self.client.get('/api/news/kelajak/').status_code, 404)
        self.assertIn('content', self.client.get('/api/news/yangi-oquv-mavsumi-qabul/').json())

    def test_team_endpoint(self):
        TeamMember.objects.create(name='Aziz Azizov', role='Direktor', bio='10 yillik tajriba', order=0)
        TeamMember.objects.create(name='Malika Karimova', role='Mentor', order=1, is_published=False)
        data = self.client.get('/api/team/').json()
        self.assertEqual([m['name'] for m in data], ['Aziz Azizov'])
        self.assertEqual(data[0]['role'], 'Direktor')
        self.assertIsNone(data[0]['photo'])
        self.assertIn('telegramUrl', data[0])

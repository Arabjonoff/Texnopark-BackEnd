import shutil
import tempfile
from datetime import timedelta
from io import BytesIO, StringIO

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import override_settings
from django.utils import timezone
from PIL import Image
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.applications.models import Application
from apps.content.models import SiteSettings
from apps.courses.models import Course
from apps.news.models import Post

API = '/api/dashboard'
MEDIA = tempfile.mkdtemp()


def png(name='rasm.png'):
    buffer = BytesIO()
    Image.new('RGB', (2, 2), 'blue').save(buffer, 'PNG')
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/png')


@override_settings(MEDIA_ROOT=MEDIA)
class DashboardApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_data', stdout=StringIO())
        User = get_user_model()
        cls.admin = User.objects.create_user('admin', password='Maxfiy-parol-123', is_staff=True)
        cls.user = User.objects.create_user('oddiy', password='Maxfiy-parol-123')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA, ignore_errors=True)

    def setUp(self):
        cache.clear()

    def login(self):
        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return token

    # --- Auth ---

    def test_login_returns_token(self):
        response = self.client.post(f'{API}/auth/login/', {'username': 'admin', 'password': 'Maxfiy-parol-123'}, format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['token']), 40)
        self.assertEqual(data['user']['username'], 'admin')
        self.assertIn('expiresAt', data)

    def test_login_rejects_wrong_password_and_non_staff(self):
        for username in ('admin', 'oddiy'):
            password = 'xato' if username == 'admin' else 'Maxfiy-parol-123'
            response = self.client.post(f'{API}/auth/login/', {'username': username, 'password': password}, format='json')
            self.assertEqual(response.json(), {'nonFieldErrors': ["Login yoki parol noto'g'ri."]})

    def test_endpoints_require_auth(self):
        self.assertEqual(self.client.get(f'{API}/courses/').status_code, 401)
        self.assertEqual(self.client.get(f'{API}/stats/').status_code, 401)

    def test_expired_token_rejected(self):
        token = self.login()
        Token.objects.filter(pk=token.pk).update(created=timezone.now() - timedelta(days=30))
        self.assertEqual(self.client.get(f'{API}/auth/me/').status_code, 401)
        self.assertFalse(Token.objects.filter(pk=token.pk).exists())

    def test_logout_deletes_token(self):
        token = self.login()
        self.assertEqual(self.client.post(f'{API}/auth/logout/').status_code, 204)
        self.assertFalse(Token.objects.filter(pk=token.pk).exists())

    # --- Stats ---

    def test_stats(self):
        self.login()
        Application.objects.create(type='contact', name='Ali', phone='+998901234567', message='Salom')
        data = self.client.get(f'{API}/stats/').json()
        self.assertEqual(data['applications']['new'], 1)
        self.assertEqual(data['applications']['last30Days'], 1)
        self.assertEqual(len(data['applications']['daily']), 30)
        self.assertEqual(data['applications']['daily'][-1]['count'], 1)
        self.assertEqual(data['courses']['total'], 5)
        self.assertEqual(len(data['recentApplications']), 1)

    # --- CRUD ---

    def test_course_create_with_curriculum_and_auto_slug(self):
        self.login()
        payload = {
            'title': "Sun'iy intellekt", 'shortDesc': 'Qisqa', 'description': "To'liq", 'icon': 'cpu',
            'theme': 'purple', 'duration': '3 oy', 'level': 'Boshlang\'ich', 'format': 'Oflayn', 'price': 'Bepul',
            'seats': 20, 'skills': ['Python', 'ML'], 'outcomes': ['Model yaratish'],
            'curriculum': [{'week': '1-hafta', 'topic': 'Kirish'}, {'week': '2-hafta', 'topic': 'Numpy'}],
        }
        response = self.client.post(f'{API}/courses/', payload, format='json')
        self.assertEqual(response.status_code, 201, response.json())
        course = Course.objects.get(slug='suniy-intellekt')
        self.assertEqual(list(course.curriculum.values_list('topic', flat=True)), ['Kirish', 'Numpy'])

        response = self.client.patch(f'{API}/courses/{course.id}/', {'curriculum': [{'week': '1', 'topic': 'Yangi'}]}, format='json')
        self.assertEqual(response.json()['curriculum'], [{'week': '1', 'topic': 'Yangi'}])

    def test_duplicate_slug_rejected(self):
        self.login()
        course = Course.objects.get(slug='python')
        response = self.client.patch(f'{API}/courses/{course.id}/', {'slug': 'flutter'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('slug', response.json())

    def test_event_end_time_validation(self):
        self.login()
        event = self.client.get(f'{API}/events/').json()['results'][0]
        response = self.client.patch(f'{API}/events/{event["id"]}/', {'startTime': '18:00', 'endTime': '09:00'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('endTime', response.json())

    def test_application_only_status_editable(self):
        self.login()
        app = Application.objects.create(type='contact', name='Ali', phone='+998901234567', message='Salom')
        response = self.client.patch(f'{API}/applications/{app.id}/', {'status': 'done', 'name': 'Boshqa', 'adminNote': "Qo'ng'iroq qilindi"}, format='json')
        self.assertEqual(response.status_code, 200)
        app.refresh_from_db()
        self.assertEqual((app.status, app.name, app.admin_note), ('done', 'Ali', "Qo'ng'iroq qilindi"))
        self.assertEqual(self.client.post(f'{API}/applications/', {}, format='json').status_code, 405)

    def test_post_image_upload_and_clear(self):
        self.login()
        response = self.client.post(f'{API}/news/', {
            'title': 'Yangi xabar', 'category': "E'lon", 'excerpt': 'Qisqa', 'content': 'Matn',
            'isPublished': 'true', 'cover': png(),
        }, format='multipart')
        self.assertEqual(response.status_code, 201, response.json())
        post = Post.objects.get(slug='yangi-xabar')
        self.assertTrue(post.cover.name.startswith('news/'))

        response = self.client.patch(f'{API}/news/{post.id}/', {'coverClear': 'true'}, format='multipart')
        self.assertEqual(response.status_code, 200, response.json())
        self.assertIsNone(response.json()['cover'])

    def test_video_story_empty_course_uses_name(self):
        self.login()
        response = self.client.post(f'{API}/video-stories/', {
            'studentName': 'Dilnoza', 'course': '', 'courseName': 'Dizayn', 'result': 'Portfolio', 'theme': 'blue',
        }, format='multipart')
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(response.json()['courseTitle'], 'Dizayn')

        response = self.client.post(f'{API}/video-stories/', {'studentName': 'X', 'course': '', 'result': 'Y'}, format='multipart')
        self.assertEqual(response.status_code, 400)

    def test_site_settings_update(self):
        self.login()
        response = self.client.patch(f'{API}/site-settings/', {'phone': '+998 99 111 22 33'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SiteSettings.load().phone, '+998 99 111 22 33')

    def test_list_pagination_and_search(self):
        self.login()
        data = self.client.get(f'{API}/courses/', {'search': 'python', 'page_size': 2}).json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['slug'], 'python')

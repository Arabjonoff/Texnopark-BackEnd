from io import StringIO
from unittest import mock

from django.core.cache import cache
from django.core.management import call_command
from rest_framework.test import APITestCase
from rest_framework.throttling import ScopedRateThrottle

from apps.events.models import Event

from .models import Application

URL = '/api/applications/'


class ApplicationApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_data', stdout=StringIO())

    def setUp(self):
        cache.clear()

    def test_course_application(self):
        response = self.client.post(URL, {'type': 'course', 'name': 'Ali', 'phone': '+998 90 123 45 67', 'course': 'python'}, format='json')
        self.assertEqual(response.status_code, 201, response.json())
        application = Application.objects.get()
        self.assertEqual(application.course.slug, 'python')
        self.assertEqual(application.status, Application.Status.NEW)

    def test_validation_errors_are_readable(self):
        response = self.client.post(URL, {'type': 'contact', 'name': '', 'phone': 'abc', 'message': ''}, format='json')
        self.assertEqual(response.status_code, 400)
        errors = response.json()
        self.assertEqual(set(errors), {'name', 'phone'})

    def test_contact_requires_message(self):
        response = self.client.post(URL, {'type': 'contact', 'name': 'Ali', 'phone': '+998901234567'}, format='json')
        self.assertEqual(response.json(), {'message': ['Xabaringizni yozing.']})

    def test_closed_event_rejected(self):
        Event.objects.filter(slug='robotics-challenge').update(status=Event.Status.CLOSED)
        response = self.client.post(URL, {'type': 'event', 'name': 'Ali', 'phone': '+998901234567', 'event': 'robotics-challenge'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('event', response.json())

    def test_unknown_course_rejected(self):
        response = self.client.post(URL, {'type': 'course', 'name': 'Ali', 'phone': '+998901234567', 'course': 'yoq'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_listing_not_allowed(self):
        self.assertEqual(self.client.get(URL).status_code, 405)

    def test_throttle_per_forwarded_ip(self):
        payload = {'type': 'contact', 'name': 'Ali', 'phone': '+998901234567', 'message': 'Salom'}

        def post(ip):
            return self.client.post(URL, payload, format='json', HTTP_X_FORWARDED_FOR=ip).status_code

        with mock.patch.object(ScopedRateThrottle, 'THROTTLE_RATES', {'applications': '2/hour'}):
            self.assertEqual([post('1.1.1.1'), post('1.1.1.1'), post('1.1.1.1')], [201, 201, 429])
            self.assertEqual(post('2.2.2.2'), 201)

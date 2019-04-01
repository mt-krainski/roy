
from time import sleep

from django.contrib.auth.models import User, Permission
from django.db.utils import IntegrityError
from django.test import TestCase
from django.contrib.gis.geos import Point
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate

from activity_logger.models import Establishment, ActivityType, Activity
from activity_logger.views import activity_manager_view


class ActivityTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username='test',
            password='test',
        )
        User.objects.create(
            username='permitted-test',
            password='test',
        )
        self.test_user = User.objects.get(username='test')
        self.permitted_test_user = User.objects.get(username='permitted-test')
        self.permitted_test_user.user_permissions.add(
            Permission.objects.get(name='Add activities via API')
        )
        self.user_token = Token.objects.get(user=self.test_user)
        self.factory = APIRequestFactory()
        Establishment.objects.create(
            name='Test',
            location=Point(0, 0),
            user=self.test_user,
        )
        ActivityType.objects.create(
            name='Test activity',
            user=self.test_user,
        )
        sleep(1)

    def test_establishment(self):
        test_item = Establishment.objects.get(name='Test')
        self.assertEqual(
            test_item.slug, 'test')

        test_item.name = 'New name'
        test_item.save()
        self.assertEqual(
            test_item.slug, 'new-name')

        now = timezone.now()
        test_item.location = Point(1, 1)
        test_item.save()
        self.assertAlmostEqual(
            test_item.updated_at.timestamp(),
            now.timestamp(),
            delta=1.0
        )

        with self.assertRaises(IntegrityError):
            Establishment.objects.create(
                name='New name',
                location=Point(0, 0),
                user=self.test_user,
            )

    def test_activity_type(self):
        test_item = ActivityType.objects.get(name='Test activity')

        self.assertEqual(
            test_item.slug, 'test-activity')

        now = timezone.now()
        test_item.name = 'New name'
        test_item.save()

        self.assertEqual(
            test_item.slug, 'new-name')

        self.assertAlmostEqual(
            test_item.updated_at.timestamp(),
            now.timestamp(),
            delta=1.0
        )

        with self.assertRaises(IntegrityError):
            Establishment.objects.create(
                name='New name',
                user=self.test_user,
            )

    def test_activity(self):
        Activity.objects.create(
            name='Test Activity',
            activity_type=ActivityType.objects.get(slug='test-activity'),
            establishment=Establishment.objects.get(slug='test'),
            user=self.test_user
        )

        test_item = Activity.objects.get(name='Test Activity')

        self.assertEqual(
            test_item.slug, 'test-activity')

    def make_activity_manager_request(self, data, user=None):

        if user is None:
            user = self.permitted_test_user

        request = self.factory.post(
            'activity_logger/activity_manager',
            data,
            format='json',
        )
        force_authenticate(
            request,
            user=user,
            token=user
        )
        response = activity_manager_view(request)
        return response

    def test_invalid_user(self):

        response = self.make_activity_manager_request({}, self.test_user)
        self.assertEqual(response.status_code, 302)

    def test_invalid_content(self):

        response = self.make_activity_manager_request(
            {'test': ''})
        self.assertEqual(response.status_code, 422)

    def test_incorrect_establishment(self):
        response = self.make_activity_manager_request(
            {
                'type': 'start',
                'establishment': 'incorrect',
                'activity_type': 'test-activity',
            }
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn(b'Establishment', response.content)

    def test_incorrect_activity_type(self):
        response = self.make_activity_manager_request(
            {
                'type': 'start',
                'establishment': 'test',
                'activity_type': 'incorrect',
            }
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn(b'Activity type', response.content)

    def test_activity_life_cycle(self):
        response = self.make_activity_manager_request(
            {
                'type': 'start',
                'establishment': 'test',
                'activity_type': 'test-activity',
            }
        )

        created_uuid = str(response.data)

        self.assertEqual(
            response.status_code, 200)
        self.assertTrue(
            Activity.objects.filter(
                name='From API',
                uuid=created_uuid,
                end_time__isnull=True
            ).exists()
        )

        response = self.make_activity_manager_request(
            {
                'type': 'finish',
                'activity_uuid': f'"{created_uuid}"',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Activity.objects.filter(
                name='From API',
                uuid=created_uuid,
                end_time__isnull=True,
            ).exists()
        )

        response = self.make_activity_manager_request(
            {
                'type': 'finish',
                'activity_uuid': f'"{created_uuid}"',
            }
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn(b'Invalid UUID', response.content)

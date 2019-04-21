from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse

from bistro.forms import PlaceForm
from bistro.models import BistroType, ConsumableType, BistroPlace, Visit


class BistroTestCase(TestCase):
    def setUp(self):
        self.bistro_type, _ = BistroType.objects.get_or_create(
            name='Test type',
            slug='other',
        )
        self.consumable_type, _ = ConsumableType.objects.get_or_create(
            name='Test consumable'
        )
        self.test_user = User.objects.create_user(
            username='test',
            password='test',
        )
        self.test_user.save()
        self.bistro_place, _ = BistroPlace.objects.get_or_create(
            name='Test place',
            location=Point(0, 0),
            user=self.test_user,
            type=self.bistro_type,
        )

        for i in range(5):
            BistroPlace.objects.get_or_create(
                name=f'Test place {i}',
                location=Point(0, 0),
                user=self.test_user,
                type=self.bistro_type,
            )

        self.visit, _ = Visit.objects.get_or_create(
            place=self.bistro_place,
            user=self.test_user,
            rating=3,
            consumable=self.consumable_type,
            price=100.0,
        )

    def test_bistro_models(self):
        self.assertEqual(repr(self.bistro_type), 'test-type')
        self.assertEqual(repr(self.consumable_type), 'test-consumable')
        self.assertEqual(repr(self.bistro_place), 'test-place')
        self.assertEqual(self.visit.get_rating_display(), '⭐⭐⭐')

        self.assertEqual(str(self.visit.place), 'Test place')
        self.assertEqual(
            str(self.visit.place.type), 'Test type')
        self.assertEqual(
            str(self.visit.consumable), 'Test consumable')

    def test_url_exists(self):
        self.client.login(
            username='test',
            password='test',
        )
        response = self.client.get(reverse('bistro:random_bistro'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'test')
        self.assertTemplateUsed(
            response, 'bistro/bistro.html')
        response = self.client.get(reverse('bistro:add_place'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'test')
        self.assertTemplateUsed(response, 'bistro/add.html')

    def test_random_bistro(self):
        self.client.login(
            username='test',
            password='test',
        )
        found_bistros = []
        for i in range(100):
            response = self.client.get(reverse('bistro:random_bistro'))
            found_bistros.append(response.context['bistro'])

        self.assertEqual(
            set(found_bistros),
            set(BistroPlace.objects.filter(user=self.test_user))
        )

    def test_add_place_form(self):
        self.client.login(
            username='test',
            password='test',
        )
        response = self.client.get(reverse('bistro:add_place'))
        self.assertIsInstance(
            response.context['form'], PlaceForm
        )

    def test_add_place(self):
        self.client.login(
            username='test',
            password='test',
        )
        response = self.client.post(
            reverse('bistro:add_place'),
            {
                'place_name': 'New Test Place',
                'type': self.bistro_type.pk,
                'location': str(Point(0, 0)),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('bistro:add_place'))

        new_place = BistroPlace.objects.filter(name='New Test Place')
        self.assertTrue(new_place.exists())

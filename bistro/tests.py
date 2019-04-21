from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.test import TestCase

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
        self.test_user, _ = User.objects.get_or_create(
            username='test',
            password='test',
        )
        self.bistro_place, _ = BistroPlace.objects.get_or_create(
            name='Test place',
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


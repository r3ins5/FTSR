from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .serializers import PerevalSerializer
from .models import *
from django.urls import reverse


class pereval_addedTestCase(APITestCase):
    def setUp(self):
        self.pereval_1 = pereval_added.objects.create(
            status='',
            tourist_id=Users.objects.create(
                email='test1@mail.ru',
                fam='Test1',
                name='Test1',
                otc='Test1',
                phone='79998887766'
            ),
            add_time='',
            beauty_title='Test1',
            title='Test1',
            other_titles='Test1',
            connect='',
            coord_id=Coords.objects.create(
                latitude=56.000000,
                longitude=65.000000,
                height=2655
            ),
            level=Level.objects.create(
                winter='4A',
                summer='',
                autumn='',
                spring=''
            ),
        )
        self.image_1 = Images.objects.create(
            image="",
            title="Test1",
        )

        self.pereval_2 = pereval_added.objects.create(
            status='',
            tourist_id=Users.objects.create(
                email='test2@mail.ru',
                fam='Test2',
                name='Test2',
                otc='Test2',
                phone='79998889988'
            ),
            add_time='',
            beauty_title='Test2',
            title='Test2',
            other_titles='Test2',
            connect='',
            coord_id=Coords.objects.create(
                latitude=98.000000,
                longitude=89.000000,
                height=4500
            ),
            level=Level.objects.create(
                winter='3A',
                summer='',
                autumn='',
                spring=''
            ),
        )
        self.image_2 = Images.objects.create(
            image="",
            title="Test2",
        )

    def test_get_list(self):
        url = reverse('pereval-list')
        response = self.client.get(url)
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.json())

    def test_get_detail(self):
        url = reverse('pereval-detail', args=(self.pereval_1.id,))
        response = self.client.get(url)
        serializer_data = PerevalSerializer(self.pereval_1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.json())


class PerevalSerializerTestCase(TestCase):
    def setUp(self):
        self.pereval_1 = pereval_added.objects.create(
            id=1,
            status='',
            tourist_id=Users.objects.create(
                email='test1@mail.ru',
                fam='Test1',
                name='Test1',
                otc='Test1',
                phone='79998887766'
            ),
            add_time='',
            beauty_title='Test1',
            title='Test1',
            other_titles='Test1',
            connect='',
            coord_id=Coords.objects.create(
                latitude=56.000000,
                longitude=65.000000,
                height=2655
            ),
            level=Level.objects.create(
                winter='4A',
                summer='',
                autumn='',
                spring=''
            ),
        )
        self.image_1 = Images.objects.create(
            image="",
            title="Test1",
        )

        self.pereval_2 = pereval_added.objects.create(
            id=2,
            status='',
            tourist_id=Users.objects.create(
                email='test2@mail.ru',
                fam='Test2',
                name='Test2',
                otc='Test2',
                phone='79998889988'
            ),
            add_time='',
            beauty_title='Test2',
            title='Test2',
            other_titles='Test2',
            connect='',
            coord_id=Coords.objects.create(
                latitude=98.000000,
                longitude=89.000000,
                height=4500
            ),
            level=Level.objects.create(
                winter='3A',
                summer='',
                autumn='',
                spring=''
            ),
        )
        self.image_2 = Images.objects.create(
            image="",
            title="Test2",
        )

    def test_check(self):
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data
        expected_data = [
            {
                'id': 1,
                'status': '',
                'tourist_id': {
                    'email': 'test1@mail.ru',
                    'fam': 'Test1',
                    'name': 'Test1',
                    'otc': 'Test1',
                    'phone': '79998887766'
                },
                'add_time': self.pereval_1.add_time.strftime('%d-%m-%Y %H:%M:%S'),
                'beauty_title': 'Test1',
                'title': 'Test1',
                'other_titles': 'Test1',
                'connect': '',
                'coord_id': {
                    'latitude': 56.000000,
                    'longitude': 65.000000,
                    'height': 2655
                },
                'level': {
                    'winter': '4A',
                    'spring': '',
                    'summer': '',
                    'autumn': '',
                },
                'images': [

                ]
            },
            {
                'id': 2,
                'status': '',
                'tourist_id': {
                    'email': 'test2@mail.ru',
                    'fam': 'Test2',
                    'name': 'Test2',
                    'otc': 'Test2',
                    'phone': '79998889988'
                },
                'add_time': self.pereval_2.add_time.strftime('%d-%m-%Y %H:%M:%S'),
                'beauty_title': 'Test2',
                'title': 'Test2',
                'other_titles': 'Test2',
                'connect': '',
                'coord_id': {
                    'latitude': 98.000000,
                    'longitude': 89.000000,
                    'height': 4500
                },
                'level': {
                    'winter': '3A',
                    'spring': '',
                    'summer': '',
                    'autumn': '',
                },
                'images': [

                ]
            },
        ]
        # print('*************************')
        # print(serializer_data)
        # print('*************************')
        # print(expected_data)
        # print('*************************')
        self.assertEqual(serializer_data, expected_data)
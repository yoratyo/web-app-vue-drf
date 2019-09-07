import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import DrillHole, DepthReading
from .serializers import DrillHoleSerializers, DepthReadingSerializers
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory


# initialize the APIClient app
client = Client()

factory = APIRequestFactory()
request = factory.get('/')

serializer_context = {
    'request': Request(request),
}

class DrillHoleTest(TestCase):
    """ Test module for drill hole API """

    def setUp(self):
        self.drill_hole_1 = DrillHole.objects.create(
            name='Drill Hole 1',
            latitude=-6.2407804,
            longitude=106.9020543,
            azimuth=100.0,
            dip=90.0,
        )
        self.drill_hole_2 = DrillHole.objects.create(
            name='Drill Hole 2',
            latitude=-6.2407804,
            longitude=106.9020543,
            azimuth=105.0,
            dip=80.0,
        )

    def test_get_all_drillholes(self):
        # get API response
        response = client.get(reverse('drillhole-list'))
        # get data from db
        drillholes = DrillHole.objects.all()
        serializer = DrillHoleSerializers(drillholes, many=True, context=serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_drillhole(self):
        response = client.get(
            reverse('drillhole-detail', kwargs={'pk':self.drill_hole_1.id}))
        drillhole = DrillHole.objects.get(id=self.drill_hole_1.id)
        serializer = DrillHoleSerializers(drillhole, context=serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_drillhole(self):
        response = client.get(
            reverse('drillhole-detail', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DepthReadingsTest(TestCase):
    """ Test module for depth reading API """

    def setUp(self):
        self.drill_hole_1 = DrillHole.objects.create(
            name='Drill Hole 1',
            latitude=-6.2407804,
            longitude=106.9020543,
            azimuth=100.0,
            dip=90.0,
        )
        self.depth1_1 = DepthReading.objects.create(
            drill_hole=self.drill_hole_1,
            depth=10.0,
            dip=88.0,
            azimuth=100.0,
            status='Trustworthy',
        )
        self.depth2_1 = DepthReading.objects.create(
            drill_hole=self.drill_hole_1,
            depth=15.0,
            dip=89.0,
            azimuth=102.0,
            status='Trustworthy',
        )

        self.drill_hole_2 = DrillHole.objects.create(
            name='Drill Hole 2',
            latitude=-6.2407804,
            longitude=106.9020543,
            azimuth=105.0,
            dip=80.0,
        )
        self.depth1_2 = DepthReading.objects.create(
            drill_hole=self.drill_hole_2,
            depth=10.0,
            dip=82.0,
            azimuth=102.0,
            status='Trustworthy',
        )
        self.depth2_2 = DepthReading.objects.create(
            drill_hole=self.drill_hole_2,
            depth=15.0,
            dip=99.0,
            azimuth=104.0,
            status='Untrustworthy',
        )

    def test_get_all_depthreadings(self):
        # get API response
        response = client.get(reverse('depthreading-list'))
        # get data from db
        depthreadings = DepthReading.objects.all()
        serializer = DepthReadingSerializers(depthreadings, many=True, context=serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_depthreading(self):
        response = client.get(
            reverse('depthreading-detail', kwargs={'pk':self.depth1_1.id}))
        depthreading = DepthReading.objects.get(id=self.depth1_1.id)
        serializer = DepthReadingSerializers(depthreading, context=serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_depthreading(self):
        response = client.get(
            reverse('depthreading-detail', kwargs={'pk': 20}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_valid_filter_depthreading_by_drillhole(self):
        response = client.get('http://localhost:8000/api/v1/depthReading/?drill_hole={}'.format(self.drill_hole_1.id))
        depthreadings = DepthReading.objects.filter(drill_hole=self.drill_hole_1.id)
        serializer = DepthReadingSerializers(depthreadings, context=serializer_context, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_depthreading(self):
        valid_payload = {
            'drill_hole':'http://localhost:8000/api/v1/drillHole/1/',
            'depth':20.0,
            'azimuth':100.0,
            'dip':90.0,
            'status':'Untrustworthy'
        }

        response = client.post(
            reverse('depthreading-list'),
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_valid_update_depthreading(self):
        valid_payload = {
            'drill_hole':'http://localhost:8000/api/v1/drillHole/1/',
            'depth':20.0,
            'azimuth':100.0,
            'dip':90.0,
            'status':'Correct'
        }

        response = client.put(
            reverse('depthreading-detail', kwargs={'pk':self.depth1_1.id}),
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

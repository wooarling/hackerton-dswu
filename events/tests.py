from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Event
import json

class EventAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        # 테스트용 이벤트 생성
        self.event = Event.objects.create(
            title='테스트 이벤트',
            description='테스트 설명',
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1),
            category='hackathon'
        )

    def test_events_list(self):
        url = reverse('events_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]['title'], self.event.title)

    def test_event_detail(self):
        url = reverse('event_detail', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], self.event.title)

    def test_event_create(self):
        url = reverse('event_create')
        start = timezone.now()
        end = start + timezone.timedelta(hours=2)
        payload = {
            'title': '새 이벤트',
            'description': '내용',
            'start_time': start.isoformat(),
            'end_time': end.isoformat(),
            'category': 'contest'
        }
        response = self.client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)  # 생성 성공이면 201 권장
        data = response.json()
        self.assertIn('id', data)
        self.assertTrue(Event.objects.filter(id=data['id']).exists())

    def test_event_update(self):
        url = reverse('event_update', args=[self.event.id])
        payload = {'title': '수정된 이벤트'}
        response = self.client.put(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, '수정된 이벤트')

    def test_event_delete(self):
        url = reverse('event_delete', args=[self.event.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)  # 삭제 성공 시 204 권장
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

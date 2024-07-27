import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task, TaskStatuses


class TaskAPIViewTests(APITestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            username='Some user',
            email='some-user@email.com',
        )
        self.client.force_authenticate(user=self.test_user)

    def test_create_task(self):
        """Ensure api creates task."""
        url = reverse('tasks-list-create')
        data = {
            'description': 'Some description',
            'scheduled': '2024-08-01:12:45'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        db_task = Task.objects.get()
        self.assertEqual(db_task.status, TaskStatuses.PLANNED)
        self.assertEqual(db_task.description, 'Some description')
        self.assertEqual(db_task.description, 'Some description')
        self.assertIsNone(db_task.done)
        self.assertEqual(
            db_task.scheduled,
            datetime.datetime(2024, 8, 1, 12, 45, tzinfo=datetime.timezone.utc),
        )
        self.assertEqual(db_task.author, self.test_user)
        self.assertIsNone(db_task.assigned)

    def test_task_list(self):
        """Ensure api returns tasks."""
        Task.objects.create(
            description='Some description',
            scheduled='2024-08-01:12:45',
            author=self.test_user,
            assigned=self.test_user,
        )
        url = reverse('tasks-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        response_task = response.data[0]
        self.assertEqual(response_task['author']['username'], 'Some user')
        self.assertEqual(response_task['assigned']['username'], 'Some user')
        self.assertEqual(response_task['spareparts'], [])
        self.assertEqual(response_task['status'], 'PL')
        self.assertEqual(response_task['description'], 'Some description')
        self.assertIsNone(response_task['done'])
        self.assertEqual(response_task['scheduled'], '2024-08-01T12:45:00Z')

    def test_task_change_status(self):
        """Ensure api changes status."""
        test_task = Task.objects.create(
            description='Some description',
            scheduled='2024-08-01:12:45',
            author=self.test_user,
            assigned=self.test_user,
        )
        self.assertEqual(test_task.status, TaskStatuses.PLANNED)
        url = reverse('tasks-change-status', args=[test_task.pk])
        response = self.client.patch(url, data={'status': 'IP'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'IP'})
        test_task.refresh_from_db()
        self.assertEqual(test_task.status, TaskStatuses.IN_PROGRESS)

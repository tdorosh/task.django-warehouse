from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task
from .models import PlannedSparepart, Sparepart


class PlannedSparepartAPIViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.test_user = User.objects.create(
            username='Some user',
            email='some-user@email.com',
        )
        self.client.force_authenticate(user=self.test_user)
        self.test_task = Task.objects.create(
            description='Some description',
            scheduled='2024-08-01:12:45',
            author=self.test_user,
        )
        self.test_sparepart = Sparepart.objects.create(
            name='Some sparepart',
            units='pcs',
            price='10.2',
        )

    def test_create_planned_sparepart(self):
        """Ensure api creates planned sparepart."""
        url = reverse('planned-spareparts-create')
        data = {
            'task': self.test_task.pk,
            'sparepart': self.test_sparepart.pk,
            'planned_amount': 10,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        db_sparepart = PlannedSparepart.objects.get()
        self.assertEqual(db_sparepart.task, self.test_task)
        self.assertEqual(db_sparepart.sparepart, self.test_sparepart)
        self.assertEqual(db_sparepart.planned_amount, 10)
        self.assertEqual(db_sparepart.current_amount, 0)

    def test_update_planned_sparepart(self):
        """Ensure api updates planned sparepart."""
        test_planned_sparepart = PlannedSparepart.objects.create(
            task=self.test_task,
            sparepart=self.test_sparepart,
            planned_amount=20,
        )
        url = reverse('planned-spareparts-detail', args=[test_planned_sparepart.pk])
        response = self.client.patch(url, data={'planned_amount': 30})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_planned_sparepart.refresh_from_db()
        self.assertEqual(test_planned_sparepart.planned_amount, 30)

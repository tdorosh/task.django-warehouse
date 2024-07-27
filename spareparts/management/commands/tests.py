from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from tasks.models import Task, TaskStatuses
from spareparts.models import Sparepart, SparepartBalance, PlannedSparepart


class DistributeSparepartBalancesCommandTests(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            username='Some user',
            email='some-user@email.com',
        )
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
        self.test_planned_sparepart = PlannedSparepart.objects.create(
            task=self.test_task,
            sparepart=self.test_sparepart,
            planned_amount=10,
            current_amount=0,
        )
        self.test_balance_sparepart = SparepartBalance.objects.create(
            sparepart=self.test_sparepart,
            amount=5,
            warehouse='Warehouse 1',
        )

    def test_distribute_sparepart_balances(self):
        """Test distribute sparepart balances."""
        call_command('distribute_sparepart_balances')
        self.test_planned_sparepart.refresh_from_db()
        self.test_balance_sparepart.refresh_from_db()
        self.assertEqual(self.test_planned_sparepart.current_amount, 5)
        self.assertEqual(self.test_balance_sparepart.amount, 0)

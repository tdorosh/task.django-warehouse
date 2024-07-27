from django.core.management.base import BaseCommand
from django.db.models import F

from spareparts.models import PlannedSparepart, SparepartBalance
from tasks.models import TaskStatuses


class Command(BaseCommand):

    help = "Distribute sparepart balances"
    output_transaction = True

    def handle(self, *args, **options):
        for planned_sparepart in Command._get_planned_spareparts():
            while planned_sparepart.current_amount != planned_sparepart.planned_amount:
                balance_spareparts = Command._get_balance_spareparts(planned_sparepart)
                if balance_spareparts.exists():
                    balance_sparepart = balance_spareparts.first()
                    useful_amount = Command._get_useful_amount(planned_sparepart, balance_sparepart)
                    self._handle_spareparts(useful_amount, planned_sparepart, balance_sparepart)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Planned sparepart {planned_sparepart} '
                            f'was successfully increased by {useful_amount} '
                            f'from {balance_sparepart}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.NOTICE(
                            f'There are no more balance spareparts to increase {planned_sparepart}. '
                            f'Current amount: {planned_sparepart.current_amount}/{planned_sparepart.planned_amount}'
                        )
                    )
                    break

    @staticmethod
    def _get_planned_spareparts():
        filters = {
            'current_amount__lt': F('planned_amount'),
        }
        exclude = {
            'task__status__in': [TaskStatuses.IN_PROGRESS, TaskStatuses.DONE],
        }
        return PlannedSparepart.objects \
            .filter(**filters) \
            .exclude(**exclude) \
            .order_by('task__scheduled') \
            .iterator()

    @staticmethod
    def _get_balance_spareparts(planned_sparepart):
        base_queryset = SparepartBalance.objects.filter(amount__gt=0)
        queryset = base_queryset.filter(sparepart=planned_sparepart.sparepart)
        if not queryset.exists():
            queryset = base_queryset.filter(
                sparepart__in=planned_sparepart.sparepart.replaceable_with.all()
            )

        return queryset

    @staticmethod
    def _handle_spareparts(useful_amount, planned_sparepart, balance_sparepart):
        planned_sparepart.current_amount += useful_amount
        planned_sparepart.save(update_fields=['current_amount'])
        balance_sparepart.amount -= useful_amount
        balance_sparepart.save(update_fields=['amount'])

    @staticmethod
    def _get_useful_amount(planned_sparepart, balance_sparepart):
        needed_amount = planned_sparepart.planned_amount - planned_sparepart.current_amount
        available_amount = balance_sparepart.amount
        return available_amount if needed_amount >= available_amount else needed_amount

from django.core.management.base import BaseCommand
from spareparts.models import PlannedSparepart


class Command(BaseCommand):

    help = "Show current amounts for all planned spareparts"

    def handle(self, *args, **options):
        planned_spareparts = PlannedSparepart.objects.order_by('task__scheduled')

        for sparepart in planned_spareparts.iterator():
            message = f'Current amount for {sparepart}: {current_amount}/{sparepart.planned_amount}'
            style = (
                self.style.WARNING(message)
                if current_amount < sparepart.planned_amount
                else self.style.SUCCESS(message)
            )
            self.stdout.write(style)

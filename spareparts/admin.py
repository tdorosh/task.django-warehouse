from django.contrib import admin

from .models import Sparepart, PlannedSparepart, SparepartBalance


admin.site.register(Sparepart)
admin.site.register(PlannedSparepart)
admin.site.register(SparepartBalance)

from rest_framework import serializers

from .models import PlannedSparepart, Sparepart


class SparepartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sparepart
        fields = '__all__'


class PlannedSparepartSerializer(serializers.ModelSerializer):

    sparepart = SparepartSerializer()

    class Meta:
        model = PlannedSparepart
        fields = '__all__'


class PlannedCreateUpdateSparepartSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlannedSparepart
        fields = '__all__'

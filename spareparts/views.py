from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import PlannedSparepart
from .serializers import PlannedSparepartSerializer, PlannedCreateUpdateSparepartSerializer


class PlannedSparepartsViewSet(viewsets.ModelViewSet):

    queryset = PlannedSparepart.objects.all()
    serializer_class = PlannedSparepartSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method != 'GET':
            serializer_class = PlannedCreateUpdateSparepartSerializer
        return serializer_class

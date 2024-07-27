from django.urls import path

from .views import PlannedSparepartsViewSet


urlpatterns = [
    path('', PlannedSparepartsViewSet.as_view({'get': 'list'}), name='planned-spareparts-list'),
    path('create/', PlannedSparepartsViewSet.as_view({'post': 'create'}), name='planned-spareparts-create'),
    path(
        '<int:pk>/',
        PlannedSparepartsViewSet.as_view(
            {
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
        name='planned-spareparts-detail',
    ),
]

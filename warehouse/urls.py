from django.contrib import admin
from django.urls import path, include

from rest_framework.authtoken import views


urlpatterns = [
    path('api/v1/tasks/', include('tasks.urls')),
    path('api/v1/planned-spareparts/', include('spareparts.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('admin/', admin.site.urls),
]

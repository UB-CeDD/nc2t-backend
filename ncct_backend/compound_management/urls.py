# backend/ncct_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from ncct_backend.compound_management import views as compound_views

router = routers.DefaultRouter()
router.register(r'compounds', compound_views.CompoundViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
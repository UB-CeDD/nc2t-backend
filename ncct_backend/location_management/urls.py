from django.urls import path
from .views import LocationListCreateView, LocationRetrieveUpdateDestroyView

urlpatterns = [
    path('locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('locations/<int:pk>/', LocationRetrieveUpdateDestroyView.as_view(), name='location-detail'),
]


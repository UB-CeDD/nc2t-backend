from django.urls import path
from .views import CompoundListCreateView, CompoundRetrieveUpdateDestroyView

urlpatterns = [
    path('compounds/', CompoundListCreateView.as_view(), name='compound-list-create'),
    # Use slug converter to support token-style string primary keys
    path('compounds/<slug:pk>/', CompoundRetrieveUpdateDestroyView.as_view(), name='compound-detail'),
]


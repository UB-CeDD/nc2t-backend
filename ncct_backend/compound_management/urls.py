from django.urls import path
from .views import CompoundListCreateView, CompoundRetrieveUpdateDestroyView

urlpatterns = [
    path('compounds/', CompoundListCreateView.as_view(), name='compound-list-create'),
    path('compounds/<int:pk>/', CompoundRetrieveUpdateDestroyView.as_view(), name='compound-detail'),
]


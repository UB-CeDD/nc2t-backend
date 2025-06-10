from django.urls import path
from .views import ReferenceListCreateView, ReferenceRetrieveUpdateDestroyView

urlpatterns = [
    path('references/', ReferenceListCreateView.as_view(), name='reference-list-create'),
    path('references/<int:pk>/', ReferenceRetrieveUpdateDestroyView.as_view(), name='reference-detail'),
]


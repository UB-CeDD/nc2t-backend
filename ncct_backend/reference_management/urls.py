from django.urls import path
from .views import ReferenceListCreateView, ReferenceRetrieveUpdateDestroyView, ReferenceSearchView

urlpatterns = [
    path('references/', ReferenceListCreateView.as_view(), name='reference-list-create'),
    path('references/<int:pk>/', ReferenceRetrieveUpdateDestroyView.as_view(), name='reference-detail'),
    path('references/search/', ReferenceSearchView.as_view(), name='reference-search'),
]


from django.urls import path
from .views import ReferenceListCreateView, ReferenceRetrieveUpdateDestroyView, ReferenceSearchView

urlpatterns = [
    path('references/', ReferenceListCreateView.as_view(), name='reference-list-create'),
    # Slug converter allows token-style string primary keys
    path('references/<slug:pk>/', ReferenceRetrieveUpdateDestroyView.as_view(), name='reference-detail'),
    path('references/search/', ReferenceSearchView.as_view(), name='reference-search'),
]


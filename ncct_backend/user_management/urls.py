from django.urls import path
from . import views

urlpatterns = [
    path('admin/login/', views.SuperAdminLoginView.as_view(), name='superadmin_login'),
    path('admin/create-user/', views.CreateUserView.as_view(), name='create_user'),
    path('user/complete-profile/', views.CompleteProfileView.as_view(), name='complete_profile'),
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/update/', views.UpdateUserView.as_view(), name='user-update'),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('users/<int:pk>/soft-delete/', views.SoftDeleteUserView.as_view(), name='user-soft-delete'),
    path('users/<int:pk>/hard-delete/', views.HardDeleteUserView.as_view(), name='user-hard-delete'),
]
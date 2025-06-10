from django.urls import path
from .views import RegisterAPI, LoginAPI, UserProfileAPI, UserListAPI, UserDetailAPI, AdminCreateUserAPI
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from django.contrib.auth.views import LogoutView as DjangoLogoutView

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('profile/', UserProfileAPI.as_view(), name='profile'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', DjangoLogoutView.as_view(), name='django-logout'),
    path('users/', UserListAPI.as_view(), name='user-list'),
    path('users/create/', AdminCreateUserAPI.as_view(), name='admin-create-user'),
    path('users/<int:user_id>/', UserDetailAPI.as_view(), name='user-detail'),
]


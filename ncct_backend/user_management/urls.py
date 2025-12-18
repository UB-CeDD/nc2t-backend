from django.urls import path, re_path
from .views import RegisterAPI, LoginAPI, UserProfileAPI, UserListAPI, UserDetailAPI, AdminUserCreateAPI, LogoutAPI
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from django.contrib.auth.views import LogoutView as DjangoLogoutView

urlpatterns = [
    re_path(r'^register/?$', RegisterAPI.as_view(), name='register'),
    re_path(r'^login/?$', LoginAPI.as_view(), name='login'),
    re_path(r'^profile/?$', UserProfileAPI.as_view(), name='profile'),
    re_path(r'^token/verify/?$', TokenVerifyView.as_view(), name='token_verify'),
    re_path(r'^token/refresh/?$', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^logout/?$', LogoutAPI.as_view(), name='logout'),
    re_path(r'^users/?$', UserListAPI.as_view(), name='user-list-create'),
    re_path(r'^users/create/?$', AdminUserCreateAPI.as_view(), name='admin-create-user'),
    re_path(r'^users/(?P<pk>\d+)/?$', UserDetailAPI.as_view(), name='user-detail'),
    re_path(r'^users/(?P<pk>\d+)/soft-delete/?$', UserDetailAPI.as_view(), name='user-soft-delete'),
    re_path(r'^users/(?P<pk>\d+)/hard-delete/?$', UserDetailAPI.as_view(), name='user-hard-delete'),
]


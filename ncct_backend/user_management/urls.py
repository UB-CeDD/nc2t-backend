# from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView
# from .views import LoginView
#
# urlpatterns = [
#     path('login/', LoginView.as_view(), name='login'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     # path('profile/', views.UserProfileView.as_view(), name='user-profile'),
#     # path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
#     # path('users/<int:pk>/update/', views.UpdateUserView.as_view(), name='user-update'),
#     # path('users/<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
#     # path('users/<int:pk>/soft-delete/', views.SoftDeleteUserView.as_view(), name='user-soft-delete'),
#     # path('users/<int:pk>/hard-delete/', views.HardDeleteUserView.as_view(), name='user-hard-delete'),
# ]


from django.urls import path
from .views import RegisterAPI, LoginAPI, UserProfileAPI, UserListAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('profile/', UserProfileAPI.as_view(), name='profile'),
    path('users/', UserListAPI.as_view(), name='user-list'),
]
# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth.models import User, Group
# from django.utils.crypto import get_random_string
# from django.core.mail import send_mail
# from django.utils import timezone
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.conf import settings
# from datetime import timedelta
# from rest_framework.permissions import IsAdminUser
# from .serializers import UserSerializer
# from rest_framework import generics
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
#
#
# class LoginView(APIView):
#     """
#     JWT Authentication endpoint for superusers.
#     Generates tokens only after successful credential validation.
#     """
#
#     def post(self, request):
#         # Debugging request data
#         print("Received login request with data:")
#         print(request.data)
#
#         email = request.data.get('email')
#         password = request.data.get('password')
#
#         # Validate required fields
#         if not email or not password:
#             return Response(
#                 {
#                     "status": "error",
#                     "message": "Both email and password are required",
#                     "code": "MISSING_CREDENTIALS"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         # Authenticate user
#         user = authenticate(username=email, password=password)
#
#         if not user:
#             return Response(
#                 {
#                     "status": "error",
#                     "message": "Invalid credentials",
#                     "code": "INVALID_CREDENTIALS"
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
#
#         if not user.is_superuser:
#             return Response(
#                 {
#                     "status": "error",
#                     "message": "Superuser privileges required",
#                     "code": "INSUFFICIENT_PRIVILEGES"
#                 },
#                 status=status.HTTP_403_FORBIDDEN
#             )
#
#         # Generate tokens only after all validations pass
#         try:
#             refresh = RefreshToken.for_user(user)
#             return Response(
#                 {
#                     "status": "success",
#                     "message": "Login successful",
#                     "data": {
#                         "refresh": str(refresh),
#                         "access": str(refresh.access_token),
#                         "user": {
#                             "id": user.id,
#                             "email": user.email,
#                             "is_superuser": user.is_superuser
#                         }
#                     }
#                 },
#                 status=status.HTTP_200_OK
#             )
#         except Exception as e:
#             print(f"Token generation error: {str(e)}")
#             return Response(
#                 {
#                     "status": "error",
#                     "message": "Could not generate access token",
#                     "code": "TOKEN_GENERATION_ERROR"
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
# class CreateUserView(APIView):
#     permission_classes = [IsAdminUser]
#
#     def post(self, request):
#         email = request.data.get('email')
#         role = request.data.get('role')
#
#         if not request.user.is_superuser:
#             return Response({"error": "Only superusers can create new users"}, status=status.HTTP_403_FORBIDDEN)
#
#         if User.objects.filter(email=email).exists():
#             return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
#
#         user = User.objects.create(username=email, email=email, is_active=False)
#         group, created = Group.objects.get_or_create(name=role)
#         user.groups.add(group)
#
#         auth_code = get_random_string(6, allowed_chars='1234567890')
#         user.profile.auth_code = auth_code
#         user.profile.auth_code_expiry = timezone.now() + timedelta(hours=1)
#         user.save()
#
#         send_mail(
#             'Complete Your Profile',
#             f'Your authentication code is {auth_code}. It is valid for 1 hour.',
#             settings.DEFAULT_FROM_EMAIL,
#             [email],
#         )
#
#         return Response({"message": "User created and email sent"}, status=status.HTTP_201_CREATED)
#
# class CompleteProfileView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         auth_code = request.data.get('auth_code')
#         first_name = request.data.get('first_name')
#         last_name = request.data.get('last_name')
#         department = request.data.get('department')
#         password = request.data.get('password')
#         confirm_password = request.data.get('confirm_password')
#
#         try:
#             user = User.objects.get(email=email)
#
#             if user.profile.auth_code != auth_code or timezone.now() > user.profile.auth_code_expiry:
#                 return Response({"error": "Invalid or expired auth code"}, status=status.HTTP_400_BAD_REQUEST)
#
#             if password != confirm_password:
#                 return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
#
#             user.first_name = first_name
#             user.last_name = last_name
#             user.profile.department = department
#             user.set_password(password)
#             user.is_active = True
#             user.profile.auth_code = None
#             user.save()
#
#             return Response({"message": "Profile completed"}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#
# class UpdateUserView(generics.UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class UserListCreateView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class SoftDeleteUserView(generics.UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def patch(self, request, *args, **kwargs):
#         user = self.get_object()
#         user.is_active = False
#         user.save()
#         return Response({"message": "User soft deleted"}, status=status.HTTP_200_OK)
#
# class HardDeleteUserView(generics.DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def delete(self, request, *args, **kwargs):
#         user = self.get_object()
#         user.delete()
#         return Response({"message": "User hard deleted"}, status=status.HTTP_204_NO_CONTENT)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny


class RegisterAPI(APIView):
    permission_classes = [AllowAny]  # Add this line

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    permission_classes = [AllowAny]  # Add this line

    def post(self, request):
        print(request.data)

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
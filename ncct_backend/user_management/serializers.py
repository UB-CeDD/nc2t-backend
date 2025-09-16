# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.utils.crypto import get_random_string
from .utils import send_welcome_email

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()

        # Assign default 'Admin' role to the user
        admin_group, created = Group.objects.get_or_create(name='Admin')
        user.groups.add(admin_group)

        return user

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active']

    def get_role(self, obj):
        if obj.groups.exists():
            return obj.groups.first().name
        return None

class AdminUserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=['Author', 'Curator', 'Publisher'], required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True}
        }

    def create(self, validated_data):
        role_name = validated_data.pop('role')
        password = validated_data.pop('password', None)
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        if not password:
            password = get_random_string(12)
            send_welcome_email(user.username, user.email, password)

        user.set_password(password)
        user.save()

        group, created = Group.objects.get_or_create(name=role_name)
        user.groups.add(group)

        return user
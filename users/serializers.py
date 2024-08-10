from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
                "max_length": 128,
                "validators": [validate_password],
                "style": {"input_type": "password", "placeholder": "Password"},
            },
            "username": {
                "required": False,
                "style": {
                    "input_type": "text",
                    "placeholder": "Username (optional)",
                },
            },
            "first_name": {
                "required": False,
                "style": {
                    "input_type": "text",
                    "placeholder": "First Name (optional)",
                },
            },
            "last_name": {
                "required": False,
                "style": {
                    "input_type": "text",
                    "placeholder": "Last Name (optional)",
                },
            },
        }


class UserManageSerializer(serializers.ModelSerializer):
    """User model serializer for managing a user profile."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "is_staff",
            "first_name",
            "last_name",
        ]


class UserUpdateSerializer(UserCreateSerializer):
    """User model serializer for updating a user profile without a password."""

    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields.copy()
        fields.remove("password")


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    """User model serializer for updating a user's password."""

    class Meta:
        model = User
        fields = ["password"]

        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
                "max_length": 128,
                "validators": [validate_password],
                "style": {"input_type": "password", "placeholder": "Password"},
            },
        }

    def update(self, instance: User, validated_data: dict) -> User:
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

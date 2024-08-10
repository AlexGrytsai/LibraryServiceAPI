import os
from urllib.request import urlopen

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.files.base import ContentFile
from rest_framework import serializers

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """User model serializer."""

    photo = serializers.ImageField(
        required=False, use_url=True, allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
            "birth_date",
            "photo",
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
            "birth_date": {
                "required": False,
                "style": {
                    "input_type": "date",
                    "placeholder": "Birth date (optional)",
                },
            },
        }

    def to_internal_value(self, data):
        mutable_data = data.copy()
        if "birth_date" in mutable_data and mutable_data["birth_date"] == "":
            mutable_data["birth_date"] = None
        if "photo" in mutable_data and mutable_data["photo"] == "":
            mutable_data["photo"] = None
        if (
            "photo" in mutable_data
            and isinstance(mutable_data["photo"], str)
            and mutable_data["photo"].startswith("http")
        ):
            try:
                response = urlopen(mutable_data["photo"])
                file_name = os.path.basename(mutable_data["photo"])
                mutable_data["photo"] = ContentFile(
                    response.read(), name=file_name
                )
            except Exception:
                raise serializers.ValidationError(
                    {"photo": "Error downloading image."}
                )
        return super().to_internal_value(mutable_data)

    def create(self, validated_data: dict) -> User:
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        if validated_data["photo"]:
            if instance.photo:
                old_name_photo = os.path.basename(instance.photo.name)
                new_name_photo = validated_data["photo"].name
                if old_name_photo == new_name_photo:
                    validated_data.pop("photo")
        return super().update(instance, validated_data)


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
            "birth_date",
            "photo",
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

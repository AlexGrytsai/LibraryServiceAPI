from typing import Type

from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from users.models import User
from users.serializers import UserManageSerializer, UserUpdateSerializer, \
    UserPasswordUpdateSerializer


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows users to be viewed or edited without a password.
    """

    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        user = self.request.user

        return (
            User.objects.all()
            .filter(id=user.id)
        )

    def get_object(self) -> User:
        return self.request.user

    def get_serializer_class(self) -> Type[Serializer]:
        if self.request.method == "GET":
            return UserManageSerializer
        return UserUpdateSerializer


class UserPasswordUpdateView(generics.UpdateAPIView):
    """
    API endpoint that allows users update their password.
    """

    serializer_class = UserPasswordUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user

# Create your views here.

from django.urls import path

from users.views import ManageUserView, UserPasswordUpdateView, UserCreateView
urlpatterns = [
    path("", UserCreateView.as_view(), name="register"),
    path("me/", ManageUserView.as_view(), name="me"),
    path("me/password/", UserPasswordUpdateView.as_view(), name="password"),
]

app_name = "users"

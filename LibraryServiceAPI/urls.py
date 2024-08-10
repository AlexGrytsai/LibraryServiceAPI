"""
URL configuration for LibraryServiceAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView,
)

urlpatterns = (
    [
        path(
            "api/v1/users/token/",
            TokenObtainPairView.as_view(),
            name="token_obtain_pair",
        ),
        path(
            "api/v1/users/token/refresh/",
            TokenRefreshView.as_view(),
            name="token_refresh",
        ),
        path(
            "api/v1/users/token/verify/",
            TokenVerifyView.as_view(),
            name="token_verify",
        ),
        path(
            "api/v1/users/token/logout/",
            LogoutView.as_view(),
            name="token_logout",
        ),
        path(
            "api/v1/doc/schema/", SpectacularAPIView.as_view(), name="schema"
        ),
        path(
            "api/v1/doc/swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path("api/v1/users/", include("users.urls", namespace="users")),
        path("api/v1/books/", include("books.urls", namespace="books")),
    ]
    + debug_toolbar_urls()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

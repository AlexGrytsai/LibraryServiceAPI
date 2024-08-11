from django.urls import include, path
from rest_framework import routers

from books.views import BookView

router = routers.DefaultRouter()
router.register("books", BookView)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "books"

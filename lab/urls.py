from django.urls import path

from lab.views import index

urlpatterns = [
    path("", index, name="index"),
]
from django.urls import path

from . import views

urlpatterns = [
    # ex: /apidnt/
    path("", views.index, name="index"),
]

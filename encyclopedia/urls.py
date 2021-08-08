from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.detail, name="detail"),
    path("error_page/<str:title>", views.error_404, name="error_page"),
]

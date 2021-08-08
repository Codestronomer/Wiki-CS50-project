from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.detail, name="detail"),
    path("error/<str:title>", views.error_404, name="error_page"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
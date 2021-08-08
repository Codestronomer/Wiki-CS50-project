from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.detail, name="detail"),
    path("wiki/<str:title>", views.random_page, name="random"),
    path("error", views.error_404, name="error_page"),
    path("create", views.create, name="create"),
    path("search", views.search_result, name="search"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
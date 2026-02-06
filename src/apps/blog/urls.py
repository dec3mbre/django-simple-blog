from django.urls import path
from . import views

app_name = "blog"  # Пространство имён для reverse()

urlpatterns = [
    path("", views.article_list, name="article_list"),
    path("article/<slug:slug>/", views.article_detail, name="article_detail"),
]
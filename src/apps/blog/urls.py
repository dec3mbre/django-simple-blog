from django.urls import path
from . import views

app_name = "blog"  # Пространство имён для reverse()

urlpatterns = [
    path("", views.index, name="index"),
    path("articles/", views.article_list, name="article_list"),
    path("article/<slug:slug>/", views.article_detail, name="article_detail"),
    path("editor/", views.article_create, name="article_create"),
    path("editor/<slug:slug>/", views.article_edit, name="article_edit"),
    path("subscribe/", views.subscribe, name="subscribe"),
]
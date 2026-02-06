from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Публичный блог — на главной странице
    path("", include("apps.blog.urls")),
]

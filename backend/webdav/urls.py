from django.urls import path
from .views.webdav import WebDAVAPI

urlpatterns = [
    path("webdav/", WebDAVAPI.as_view()),
    path("webdav/<path:path>", WebDAVAPI.as_view()),
]

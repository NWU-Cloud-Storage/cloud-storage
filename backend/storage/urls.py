from django.urls import path
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from storage.views.storage import StorageAPI, MyStorageMove, MyStorageCopy, MyStorageFiles
from storage.views.storage import StorageManageViewSet

manage_router = DefaultRouter()
manage_router.register('storage', StorageManageViewSet, basename='storage')
urlpatterns = [
    url(r'^', include(manage_router.urls)),
    path("storage/", StorageAPI.as_view()),
    path("storage/<int:storage_id>/", StorageAPI.as_view()),
    path("storage/<int:storage_id>/<int:identifier_id>/", StorageAPI.as_view()),
    path("storage/<int:storage_id>/move/", MyStorageMove.as_view()),
    path("storage/<int:storage_id>/copy/", MyStorageCopy.as_view()),
    path("storage/upload/<int:storage_id>/<int:identifier_id>/", MyStorageFiles.as_view()),
    path("storage/upload/<int:storage_id>/", MyStorageFiles.as_view()),
    path("storage/download/<int:src_cata_id>/", MyStorageFiles.as_view()),
]

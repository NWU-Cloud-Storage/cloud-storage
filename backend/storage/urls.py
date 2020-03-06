from django.urls import path

from storage.views.storage import StorageAPI, MyStorageMove, MyStorageCopy, MyStorageFiles

urlpatterns = [
    path("storage/", StorageAPI.as_view()),
    path("storage/<int:storage_id>/", StorageAPI.as_view()),
    path("storage/<int:storage_id>/<int:identifier_id>/", StorageAPI.as_view()),
    path("storage/<int:storage_id>/move/", MyStorageMove.as_view()),
    path("storage/<int:storage_id>/copy/", MyStorageCopy.as_view()),
    path("storage/upload/", MyStorageFiles.as_view()),
    path("storage/upload/<int:src_cata_id>/", MyStorageFiles.as_view()),
    path("storage/download/<int:src_cata_id>/", MyStorageFiles.as_view()),
    path("group-storage/<int:group_id>/download/<int:src_cata_id>/", MyStorageFiles.as_view()),

]

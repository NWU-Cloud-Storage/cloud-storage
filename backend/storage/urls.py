from django.urls import path

from storage.views.storage import StorageAPI, MyStorageMove, MyStorageCopy, MyStorageFiles
from storage.views.group_storage import GroupStorage, GroupStorageMove, GroupStorageCopy
from storage.views.cross_storage import SaveToMe, UploadToGroup

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

    path("group-storage/<int:group_id>/", GroupStorage.as_view()),
    path("group-storage/<int:group_id>/<int:src_cata_id>/", GroupStorage.as_view()),
    path("group-storage/move/<int:group_id>/", GroupStorageMove.as_view()),
    path("group-storage/copy/<int:group_id>/", GroupStorageCopy.as_view()),

    path("save-to-me/<int:group_id>/", SaveToMe.as_view()),
    path("save-to-me/<int:group_id>/<int:des_id>/", SaveToMe.as_view()),
    path("upload-to-group/<int:group_id>/", UploadToGroup.as_view()),
    path("upload-to-group/<int:group_id>/<int:des_id>/", UploadToGroup.as_view()),
]

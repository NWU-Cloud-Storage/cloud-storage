from django.urls import path

from storage.views.my_storage import MyStorage, MyStorageMove, MyStorageCopy, MyStorageFiles
from storage.views.group_storage import GroupStorage, GroupStorageMove, GroupStorageCopy
from storage.views.cross_storage import SaveToMe, UploadToGroup


urlpatterns = [
    path("my-storage/", MyStorage.as_view()),
    path("my-storage/<int:src_cata_id>/", MyStorage.as_view()),
    path("my-storage/move/", MyStorageMove.as_view()),
    path("my-storage/copy/", MyStorageCopy.as_view()),
    path("my-storage/upload/", MyStorageFiles.as_view()),
    path("my-storage/upload/<int:src_cata_id>/", MyStorageFiles.as_view()),
    path("my-storage/download/<int:src_cata_id>/", MyStorageFiles.as_view()),
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

from django.urls import path
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from storage.views.storage import StorageAPI, MyStorageMove, MyStorageCopy, MyStorageFiles, GetPermissionsAPI
from storage.views.storage import StorageManageViewSet
from storage.views.storage_member import StorageMemberManageAPI

router = DefaultRouter()
router.register('storage', StorageManageViewSet, basename='storage')
urlpatterns = [
    path("storage/permissions/", GetPermissionsAPI.as_view()),
    path("storage/<int:storage_id>/<int:identifier_id>/", StorageAPI.as_view()),
    path("storage/<int:storage_id>/<int:identifier_id>/move/", MyStorageMove.as_view()),
    path("storage/<int:storage_id>/<int:identifier_id>/copy/", MyStorageCopy.as_view()),
    path("storage/upload/<int:storage_id>/<int:identifier_id>/", MyStorageFiles.as_view()),
    path("storage/upload/<int:storage_id>/", MyStorageFiles.as_view()),
    path("storage/download/<int:src_cata_id>/", MyStorageFiles.as_view()),

    path("storage/<int:storage_id>/member/", StorageMemberManageAPI.as_view()),
    path("storage/<int:storage_id>/member/<str:username>/", StorageMemberManageAPI.as_view()),
    url(r'^', include(router.urls)),
]

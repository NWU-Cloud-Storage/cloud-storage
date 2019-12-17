from django.urls import path

from share.views.share import ShareToPublic, ShareToMe, Share

urlpatterns = [
    path("share-to-public/<int:src_id>/", ShareToPublic.as_view()),
    path("share/<str:url>/", Share.as_view()),
    path("share/<str:url>/<int:cata_id>/", Share.as_view()),
    path("share-to-me/<str:url>/<int:src_id>/", ShareToMe.as_view()),
    path("share-to-me/<str:url>/<int:src_id>/<int:des_id>/", ShareToMe.as_view())
]

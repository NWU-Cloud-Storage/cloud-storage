from django.urls import path

from group.views.my_group import MyGroup
from group.views.membership import Membership
from group.views.intention import Intention


urlpatterns = [
    path("my-group/", MyGroup.as_view()),
    path("my-group/<int:group_id>/", MyGroup.as_view()),

    path("membership/<int:group_id>/<str:username>/", Membership.as_view()),

    path("intention/<int:group_id>/", Intention.as_view()),
    path("intention/<int:group_id>/<str:username>/", Intention.as_view()),
]

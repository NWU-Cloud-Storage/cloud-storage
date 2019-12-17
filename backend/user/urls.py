from django.urls import path
from user.views.user import User
from user.views.token import OAuthToken


urlpatterns = [
    path("user/", User.as_view()),
    path("user/<str:username>/", User.as_view()),
    path("login/<str:code>/", OAuthToken.as_view())
]

from django.urls import path
from user.views.user import User
from user.views.login import OAuthLogin, Logout

urlpatterns = [
    path("user/", User.as_view()),
    path("user/<str:username>/", User.as_view()),
    path("login/<str:code>/", OAuthLogin.as_view()),
    path("logout/", Logout.as_view())
]

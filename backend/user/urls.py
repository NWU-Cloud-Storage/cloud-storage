from django.urls import path
from user.views.user import User



urlpatterns = [
    path("user/", User.as_view()),
    path("user/<str:username>/", User.as_view())
]

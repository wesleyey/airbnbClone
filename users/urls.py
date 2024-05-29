from django.urls import path
from .views import Me, Users, PublicUser, ChangePassword, LogIn, LogOut

urlpatterns = [
    path("", Users.as_view()),
    path("me", Me.as_view()),
    path("change-password", ChangePassword.as_view()),
    path("log-in", LogIn.as_view()),
    path("log-out", LogOut.as_view()),
    path(
        "@<str:username>", PublicUser.as_view()
    ),  # 이 줄이 먼저 올라가 있으면 me가 에러남
]

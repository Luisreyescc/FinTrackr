from django.urls import path
from .views import RegisterView, LoginView, ProfileView, user_list

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("users/", user_list, name="user_list"),
    path("profile-details/", ProfileView.as_view(), name="profile-details"),
]

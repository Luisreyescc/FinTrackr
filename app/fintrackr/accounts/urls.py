from django.urls import path
from .views import UserProfileUpdateView

urlpatterns = [
    path("profile-details/", UserProfileUpdateView.as_view(), name="edit_profile"),
]

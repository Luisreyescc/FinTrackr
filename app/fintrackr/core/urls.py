from django.urls import path
from .views import RegisterView, LoginView, ProfileView, user_list, UserProfileView, IncomeDetailView, IncomeListCreateView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("users/", user_list, name="user_list"),
    path("profile-details/", ProfileView.as_view(), name="profile-details"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),

    #income views
    path("incomes/", IncomeListCreateView.as_view(), name="income-list-create"),
    path("incomes/<int:income_id>/", IncomeDetailView.as_view(), name="income-detail"),
]

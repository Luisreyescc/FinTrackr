from django.urls import path, include
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    user_list,
    UserProfileView,
    IncomeDetailView,
    IncomeListCreateView,
    IncomeSourceSummaryView,
    UserIncomeCategoriesView,
    CategoryListCreateView,
    ExpenseDetailView,
    ExpenseListCreateView,
    ExpenseCategorySummaryView,
    UserExpenseCategoriesView,
)

urlpatterns = [
    # User views
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("users/", user_list, name="user_list"),
    path("profile-details/", ProfileView.as_view(), name="profile-details"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    # income views
    path("incomes/", IncomeListCreateView.as_view(), name="income-list-create"),
    path("incomes/categories-summary/", IncomeSourceSummaryView.as_view(), name="income-source-summary"),
    path("incomes/<int:income_id>/", IncomeDetailView.as_view(), name="income-detail"),
    path("income-categories/", UserIncomeCategoriesView.as_view(), name="user-categories"),
    # Category views
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    # Expense views
    path("expenses/", ExpenseListCreateView.as_view(), name="expense-list-create"),
    path("expenses/category-summary/", ExpenseCategorySummaryView.as_view(), name="expense-category-summary",),
    path("expenses/<int:expense_id>/", ExpenseDetailView.as_view(), name="expense-detail"),
    path("expense-categories/", UserExpenseCategoriesView.as_view(), name="user-categories"),
]

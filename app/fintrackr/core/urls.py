from django.urls import path, include
from .views import (
    user_financial,
    RegisterView,
    LoginView,
    ProfileView,
    user_list,
    UserProfileView,
    IncomeDetailView,
    IncomeListCreateView,
    IncomeSourceSummaryView,
    UserIncomeCategoriesView,
    FilteredIncomeListView,
    CategoryListCreateView,
    ExpenseDetailView,
    ExpenseListCreateView,
    ExpenseCategorySummaryView,
    UserExpenseCategoriesView,
    FilteredExpenseListView,
    DebtListCreateView,
    DebtDetailView,
    DebtCategorySummaryView,
    UserDebtCategoriesView,
)

urlpatterns = [
    # Admin views
    path("admin/financial-summary/", user_financial, name="user_financial_summary"),    
    # User views
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("users/", user_list, name="user_list"),
    path("profile-details/", ProfileView.as_view(), name="profile-details"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    # income views
    path("incomes/", IncomeListCreateView.as_view(), name="income-list-create"),
    path(
        "incomes/categories-summary/",
        IncomeSourceSummaryView.as_view(),
        name="income-source-summary",
    ),
    path("incomes/<int:income_id>/",
         IncomeDetailView.as_view(), name="income-detail"),
    path(
        "income-categories/", UserIncomeCategoriesView.as_view(), name="user-categories"
    ),
    path(
        "incomes/filtered/",
        FilteredIncomeListView.as_view(),
        name="filtered-income-list",
    ),
    # Category views
    path("categories/", CategoryListCreateView.as_view(),
         name="category-list-create"),
    # Expense views
    path("expenses/", ExpenseListCreateView.as_view(), name="expense-list-create"),
    path(
        "expenses/category-summary/",
        ExpenseCategorySummaryView.as_view(),
        name="expense-category-summary",
    ),
    path(
        "expenses/<int:expense_id>/", ExpenseDetailView.as_view(), name="expense-detail"
    ),
    path(
        "expense-categories/",
        UserExpenseCategoriesView.as_view(),
        name="user-categories",
    ),
    path(
        "expenses/filtered/",
        FilteredExpenseListView.as_view(),
        name="filtered-expense-list",
    ),
    # Debt views
    path("debts/", DebtListCreateView.as_view(), name="debt-list-create"),
    path("debts/<int:debt_id>/", DebtDetailView.as_view(), name="debt-detail"),
    path(
        "debts/category-summary/",
        DebtCategorySummaryView.as_view(),
        name="debt-category-summary",
    ),
    path(
        "debt-categories/",
        UserDebtCategoriesView.as_view(),
        name="user-debt-categories",
    ),
    # Emails views
    path("", include("emails.urls")),
]


from django.urls import path
from fintrackr.core import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("users/", views.UsersListView.as_view(), name="users-list"),
    path("users/<int:pk>/", views.UsersDetailView.as_view(), name="users-detail"),
    path("incomes/", views.IncomesListView.as_view(), name="incomes-list"),
    path("incomes/<int:pk>/", views.IncomesDetailView.as_view(), name="incomes-detail"),
    path("categories/", views.CategoriesListView.as_view(), name="categories-list"),
    path(
        "categories/<int:pk>/",
        views.CategoriesDetailView.as_view(),
        name="categories-detail",
    ),
    path("expenses/", views.ExpensesListView.as_view(), name="expenses-list"),
    path(
        "expenses/<int:pk>/", views.ExpensesDetailView.as_view(), name="expenses-detail"
    ),
    path(
        "expense-categories/",
        views.ExpenseCategoriesListView.as_view(),
        name="expensecategories-list",
    ),
    path(
        "expense-categories/<int:pk>/",
        views.ExpenseCategoriesDetailView.as_view(),
        name="expensecategories-detail",
    ),
    path("debts/", views.DebtsListView.as_view(), name="debts-list"),
    path("debts/<int:pk>/", views.DebtsDetailView.as_view(), name="debts-detail"),
    path(
        "debt-categories/",
        views.DebtCategoriesListView.as_view(),
        name="debtcategories-list",
    ),
    path(
        "debt-categories/<int:pk>/",
        views.DebtCategoriesDetailView.as_view(),
        name="debtcategories-detail",
    ),
]

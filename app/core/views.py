from rest_framework import generics
from core.models import (
    Users,
    Incomes,
    Categories,
    Expenses,
    ExpenseCategories,
    Debts,
    DebtCategories,
)
from core.serializers import (
    UsersSerializer,
    IncomesSerializer,
    CategoriesSerializer,
    ExpensesSerializer,
    ExpenseCategoriesSerializer,
    DebtsSerializer,
    DebtCategoriesSerializer,
)


class UsersListView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class UsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class IncomesListView(generics.ListCreateAPIView):
    queryset = Incomes.objects.all()
    serializer_class = IncomesSerializer


class IncomesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incomes.objects.all()
    serializer_class = IncomesSerializer


class CategoriesListView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class CategoriesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class ExpensesListView(generics.ListCreateAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer


class ExpensesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer


class ExpenseCategoriesListView(generics.ListCreateAPIView):
    queryset = ExpenseCategories.objects.all()
    serializer_class = ExpenseCategoriesSerializer


class ExpenseCategoriesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExpenseCategories.objects.all()
    serializer_class = ExpenseCategoriesSerializer


class DebtsListView(generics.ListCreateAPIView):
    queryset = Debts.objects.all()
    serializer_class = DebtsSerializer


class DebtsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Debts.objects.all()
    serializer_class = DebtsSerializer


class DebtCategoriesListView(generics.ListCreateAPIView):
    queryset = DebtCategories.objects.all()
    serializer_class = DebtCategoriesSerializer


class DebtCategoriesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DebtCategories.objects.all()
    serializer_class = DebtCategoriesSerializer

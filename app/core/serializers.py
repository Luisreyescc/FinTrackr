from rest_framework import serializers
from core.models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


class IncomesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incomes
        fields = "__all__"


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = "__all__"


class ExpenseCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategories
        fields = "__all__"


class DebtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debts
        fields = "__all__"


class DebtCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtCategories
        fields = "__all__"

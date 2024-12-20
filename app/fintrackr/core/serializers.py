from rest_framework import serializers
from django.db.models import Sum
from .models import (
    Users,
    Incomes,
    Categories,
    Expenses,
    ExpenseCategories,
    IncomeCategories,
    Debts,
    DebtCategories,
)
from django.contrib.auth import authenticate


class AdminUserSerializer(serializers.ModelSerializer):
    incomes = serializers.SerializerMethodField()
    expenses = serializers.SerializerMethodField()
    debts = serializers.SerializerMethodField()
    network = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = [
            "user_id",
            "user_name",
            "email",
            "name",
            "last_name",
            "phone",
            "curp",
            "rfc",
            "birth_date",
            "incomes",
            "expenses",
            "debts",
            "network",
            "is_staff"
        ]

    def get_incomes(self, obj):
        return Incomes.objects.filter(user=obj).aggregate(total=Sum('amount'))['total'] or 0

    def get_expenses(self, obj):
        return Expenses.objects.filter(user=obj).aggregate(total=Sum('amount'))['total'] or 0

    def get_debts(self, obj):
        return Debts.objects.filter(user=obj).aggregate(total=Sum('amount'))['total'] or 0

    def get_network(self, obj):
        incomes = self.get_incomes(obj)
        expenses = self.get_expenses(obj)
        return incomes - expenses


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "username", "email"]


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        user = authenticate(
            username=attrs["user_name"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError(
                {"detail": "Invalid credentials.."})
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "user_id",
            "user_name",
            "email",
            "name",
            "last_name",
            "phone",
            "curp",
            "rfc",
            "birth_date",
        ]
        read_only_fields = ["user_id", "user_name", "email"]


class UpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    new_password = serializers.CharField(
        write_only=True, required=False, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        write_only=True, required=False, style={"input_type": "password"}
    )

    class Meta:
        model = Users
        fields = [
            "user_name",
            "name",
            "last_name",
            "email",
            "phone",
            "curp",
            "rfc",
            "birth_date",
            "password",
            "new_password",
            "confirm_password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user = self.instance
        if not user.check_password(data.get("password")):
            raise serializers.ValidationError({"password": "Current password is incorrect"})
        
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        
        if new_password or confirm_password:
            if new_password != confirm_password:
                raise serializers.ValidationError({"new_password": "New passwords do not match"})
        
        return data

    def update(self, instance, validated_data):
        validated_data.pop("password", None)  # Remove the current password from the validated data
        new_password = validated_data.pop("new_password", None)
        if new_password:
            instance.set_password(new_password)
        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.ReadOnlyField()

    class Meta:
        model = Categories
        fields = ["category_id", "name"]


# Income Serializer
class IncomeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    category = serializers.ListField(
        child=serializers.CharField(), write_only=True, source="categories"
    )
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Incomes
        fields = [
            "income_id",
            "user",
            "amount",
            "description",
            "date",
            "icon",
            "category",
            "categories",
        ]

    def get_categories(self, obj):
        return obj.incomecategories_set.values_list("category__name", flat=True)

    def create(self, validated_data):
        category_names = validated_data.pop("categories", None)

        income = Incomes.objects.create(**validated_data)

        for category_name in category_names:
            category, created = Categories.objects.get_or_create(
                name=category_name)
            IncomeCategories.objects.create(income=income, category=category)

        return income

    def update(self, instance, validated_data):
        category_names = validated_data.pop("categories", None)
        if category_names is not None:
            IncomeCategories.objects.filter(income=instance).delete()
            for category_name in category_names:
                category, created = Categories.objects.get_or_create(
                    name=category_name)
                IncomeCategories.objects.create(
                    income=instance, category=category)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class IncomeCategorySerializer(serializers.ModelSerializer):
    income = serializers.PrimaryKeyRelatedField(queryset=Incomes.objects.all())
    category = serializers.PrimaryKeyRelatedField(
        queryset=Categories.objects.all())

    class Meta:
        model = IncomeCategories
        fields = ["income", "category"]


# Expense Serializer
class ExpenseCategorySerializer(serializers.ModelSerializer):
    expense = serializers.PrimaryKeyRelatedField(
        queryset=Expenses.objects.all())
    category = serializers.PrimaryKeyRelatedField(
        queryset=Categories.objects.all())

    class Meta:
        model = ExpenseCategories
        fields = ["expense", "category"]


class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    category = serializers.ListField(
        child=serializers.CharField(), write_only=True, source="categories"
    )
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Expenses
        fields = [
            "expense_id",
            "user",
            "amount",
            "description",
            "date",
            "icon",
            "category",
            "categories",
        ]

    def get_categories(self, obj):
        return obj.expensecategories_set.values_list("category__name", flat=True)

    def create(self, validated_data):
        category_names = validated_data.pop(
            "categories", None
        )  # Changed from 'category' to 'categories'

        if not category_names:
            raise serializers.ValidationError(
                {"categories": "Este campo es requerido."}
            )

        expense = Expenses.objects.create(**validated_data)

        for category_name in category_names:
            category, created = Categories.objects.get_or_create(
                name=category_name)
            ExpenseCategories.objects.create(
                expense=expense, category=category)

        return expense

    def update(self, instance, validated_data):
        category_names = validated_data.pop(
            "categories", None
        )  # Changed from 'category' to 'categories'
        if category_names is not None:
            # Remove old categories and replace with new ones
            ExpenseCategories.objects.filter(expense=instance).delete()
            for category_name in category_names:
                category, created = Categories.objects.get_or_create(
                    name=category_name)
                ExpenseCategories.objects.create(
                    expense=instance, category=category)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# Debts Serializer
class DebtCategorySerializer(serializers.ModelSerializer):
    debt = serializers.PrimaryKeyRelatedField(queryset=Debts.objects.all())
    category = serializers.PrimaryKeyRelatedField(
        queryset=Categories.objects.all())

    class Meta:
        model = DebtCategories
        fields = ["debt", "category"]


class DebtSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    category = serializers.ListField(
        child=serializers.CharField(), write_only=True, source="categories"
    )
    categories = serializers.SerializerMethodField()
    is_payed = serializers.BooleanField()

    class Meta:
        model = Debts
        fields = [
            "debt_id",
            "user",
            "debtor_name",
            "amount",
            "description",
            "date",
            "icon",
            "is_payed",
            "category",
            "categories",
        ]

    def get_categories(self, obj):
        return obj.debtcategories_set.values_list("category__name", flat=True)

    def create(self, validated_data):
        category_names = validated_data.pop("categories", None)

        if not category_names:
            raise serializers.ValidationError(
                {"categories": "Este campo es requerido."}
            )

        debt = Debts.objects.create(**validated_data)

        for category_name in category_names:
            category, created = Categories.objects.get_or_create(
                name=category_name)
            DebtCategories.objects.create(debt=debt, category=category)

        return debt

    def update(self, instance, validated_data):
        category_names = validated_data.pop("categories", None)

        if category_names is not None:
            DebtCategories.objects.filter(debt=instance).delete()
            for category_name in category_names:
                category, created = Categories.objects.get_or_create(
                    name=category_name)
                DebtCategories.objects.create(debt=instance, category=category)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

from rest_framework import serializers
from .models import Users, Incomes, Categories, Expenses, ExpenseCategories
from django.contrib.auth import authenticate


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "username", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ["user_name", "email", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = Users.objects.create_user(
            user_name=validated_data["user_name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        user = authenticate(username=attrs["user_name"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError({"detail": "Invalid credentials.."})
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
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incomes
        fields = ["income_id", "user", "amount", "description", "date", "source"]
        read_only_fields = ["user"]


class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.ReadOnlyField()

    class Meta:
        model = Categories
        fields = ["category_id", "name"]


class ExpenseCategorySerializer(serializers.ModelSerializer):
    expense = serializers.PrimaryKeyRelatedField(queryset=Expenses.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all())

    class Meta:
        model = ExpenseCategories
        fields = ['expense', 'category']


class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    category = serializers.CharField(write_only=True)  # Expect 'category' as an input field

    class Meta:
        model = Expenses
        fields = ['expense_id', 'user', 'amount', 'description', 'date', 'category']

    def create(self, validated_data):

        category_name = validated_data.pop('category', None)

        if category_name is None:
            raise serializers.ValidationError({"category": "This field is required."})

        category, created = Categories.objects.get_or_create(name=category_name)

        expense = Expenses.objects.create(**validated_data)

        ExpenseCategories.objects.create(expense=expense, category=category)

        return expense
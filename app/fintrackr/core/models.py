from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models


class UsersManager(BaseUserManager):
    def create_user(self, user_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email is required")
        if not user_name:
            raise ValueError("The username is required")

        email = self.normalize_email(email)
        user = self.model(user_name=user_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("The superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("The superuser must have is_superuser=True.")

        return self.create_user(user_name, email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=18, blank=True, null=True)
    curp = models.CharField(max_length=18, unique=True, blank=True, null=True)
    rfc = models.CharField(max_length=18, unique=True, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsersManager()

    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = ["email", "name", "last_name"]

    def __str__(self):
        return self.user_name

    @property
    def id(self):
        return self.user_id


class Incomes(models.Model):
    income_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    source = models.CharField(max_length=255, null=True, blank=True)


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)


class Expenses(models.Model):
    expense_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()


class ExpenseCategories(models.Model):
    expense = models.ForeignKey(Expenses, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

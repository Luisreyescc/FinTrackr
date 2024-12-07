from rest_framework import generics, permissions, status, viewsets
from django.db.models import Sum
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from datetime import datetime, timedelta
from .models import (
    Users,
    Incomes,
    IncomeCategories,
    Categories,
    Expenses,
    ExpenseCategories,
)
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UpdateUserSerializer,
    IncomeSerializer,
    CategorySerializer,
    ExpenseSerializer,
)

# Admin / Super user views
@api_view(["GET"])
@permission_classes([IsAdminUser])
def user_financial(request):
    users = Users.objects.all()
    user_data = []

    for user in users:
        incomes = Incomes.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        expenses = Expenses.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        debts = 0  # Assuming you have a model for debts, replace this with the actual calculation
        network = incomes - expenses

        user_info = {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "email": user.email,
            "name": user.name,
            "last_name": user.last_name,
            "phone": user.phone,
            "curp": user.curp,
            "rfc": user.rfc,
            "birth_date": user.birth_date,
            "incomes": float(incomes),
            "expenses": float(expenses),
            "debts": float(debts),
            "network": float(network)
        }
        user_data.append(user_info)

    return Response(user_data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_user(request, user_id):
    try:
        user = Users.objects.get(user_id=user_id)
        email = user.email
        user_name = user.user_name

        Incomes.objects.filter(user=user).delete()
        Expenses.objects.filter(user=user).delete()
        # Assuming you have a model for debts, add the deletion here
        # Debts.objects.filter(user=user).delete()

        user.delete()

        send_mail(
            subject="User Account Deleted",
            message=f"Dear {user_name},\n\nYour user account has been removed. Thank you for using our service.\n\nBest regards,\nYour Company",
            from_email=None,
            recipient_list=[email],
        )

        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Users.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


# User views
@api_view(["GET"])
@permission_classes([AllowAny])
def user_list(request):
    users = Users.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "is_admin": user.is_staff,
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateUserSerializer
        return UserSerializer


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"user_name": user.user_name})


# Income views
class IncomeListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        incomes = Incomes.objects.filter(user=request.user)
        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncomeDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, income_id, user):
        try:
            return Incomes.objects.get(pk=income_id, user=user)
        except Incomes.DoesNotExist:
            return None

    def get(self, request, income_id):
        income = self.get_object(income_id, request.user)
        if not income:
            return Response(
                {"error": "Income not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = IncomeSerializer(income)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, income_id):
        income = self.get_object(income_id, request.user)
        if not income:
            return Response(
                {"error": "Income not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = IncomeSerializer(income, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, income_id):
        income = self.get_object(income_id, request.user)
        if not income:
            return Response(
                {"error": "Income not found."}, status=status.HTTP_404_NOT_FOUND
            )
        income.delete()
        return Response(
            {"message": "Income deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class IncomeSourceSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories_summary = (
            IncomeCategories.objects.filter(income__user=request.user)
            .values("category__name")
            .annotate(total_amount=Sum("income__amount"))
            .order_by("category__name")
        )

        response_data = [
            {
                "category": category["category__name"],
                "total_amount": category["total_amount"],
            }
            for category in categories_summary
        ]

        return Response(response_data, status=status.HTTP_200_OK)


class UserIncomeCategoriesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = (
            IncomeCategories.objects.filter(income__user=request.user)
            .values_list("category__name", flat=True)
            .distinct()
        )
        return Response({"categories": list(categories)}, status=status.HTTP_200_OK)


# Expense views
class ExpenseListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        expenses = Expenses.objects.filter(user=request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, expense_id, user):
        try:
            return Expenses.objects.get(pk=expense_id, user=user)
        except Expenses.DoesNotExist:
            return None

    def get(self, request, expense_id):
        expense = self.get_object(expense_id, request.user)
        if not expense:
            return Response(
                {"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, expense_id):
        expense = self.get_object(expense_id, request.user)
        if not expense:
            return Response(
                {"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, expense_id):
        expense = self.get_object(expense_id, request.user)
        if not expense:
            return Response(
                {"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND
            )

        expense.delete()
        return Response(
            {"message": "Expense deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # Make this view publicly accessible


class ExpenseCategorySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories_summary = (
            ExpenseCategories.objects.filter(expense__user=request.user)
            .values("category__name")
            .annotate(total_amount=Sum("expense__amount"))
            .order_by("category__name")
        )

        response_data = [
            {
                "category": category["category__name"],
                "total_amount": category["total_amount"],
            }
            for category in categories_summary
        ]

        return Response(response_data, status=status.HTTP_200_OK)


class UserExpenseCategoriesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = (
            ExpenseCategories.objects.filter(expense__user=request.user)
            .values_list("category__name", flat=True)
            .distinct()
        )
        return Response({"categories": list(categories)}, status=status.HTTP_200_OK)


# Filtered views
class FilteredIncomeListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        filter_type = request.query_params.get('filter', 'All')
        date_str = request.query_params.get('date', None)

        if filter_type != 'All' and not date_str:
            return Response(
                {"error": "Date is required for the selected filter."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if filter_type == 'All':
            incomes = Incomes.objects.filter(user=request.user)
        else:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if filter_type == 'Day':
                start_date = date
                end_date = date + timedelta(days=1)
            elif filter_type == 'Month':
                start_date = date.replace(day=1)
                end_date = (start_date + timedelta(days=32)).replace(day=1)
            elif filter_type == 'Year':
                start_date = date.replace(month=1, day=1)
                end_date = date.replace(year=date.year + 1, month=1, day=1)
            elif filter_type == 'Fortnight':
                if date.day <= 15:
                    start_date = date.replace(day=1)
                    end_date = date.replace(day=15)
                else:
                    start_date = date.replace(day=16)
                    end_date = (start_date + timedelta(days=15)).replace(day=1)
            else:
                start_date = date
                end_date = date + timedelta(days=1)

            incomes = Incomes.objects.filter(user=request.user, date__range=[start_date, end_date])

        total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        categories_summary = (
            IncomeCategories.objects.filter(income__in=incomes)
            .values("category__name")
            .annotate(total_amount=Sum("income__amount"))
            .order_by("category__name")
        )

        # Sum incomes by date
        income_data = incomes.values('date').annotate(total_amount=Sum('amount')).order_by('date')

        response_data = {
            'incomes': [{'x': item['date'], 'y': item['total_amount']} for item in income_data],
            'total_income': total_income,
            'categories_summary': [
                {
                    "category": category["category__name"],
                    "total_amount": category["total_amount"],
                }
                for category in categories_summary
            ]
        }

        return Response(response_data)


class FilteredExpenseListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        filter_type = request.query_params.get('filter', 'All')
        date_str = request.query_params.get('date', None)

        if filter_type != 'All' and not date_str:
            return Response(
                {"error": "Date is required for the selected filter."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if filter_type == 'All':
            expenses = Expenses.objects.filter(user=request.user)
        else:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if filter_type == 'Day':
                start_date = date
                end_date = date + timedelta(days=1)
            elif filter_type == 'Month':
                start_date = date.replace(day=1)
                end_date = (start_date + timedelta(days=32)).replace(day=1)
            elif filter_type == 'Year':
                start_date = date.replace(month=1, day=1)
                end_date = date.replace(year=date.year + 1, month=1, day=1)
            elif filter_type == 'Fortnight':
                if date.day <= 15:
                    start_date = date.replace(day=1)
                    end_date = date.replace(day=15)
                else:
                    start_date = date.replace(day=16)
                    end_date = (start_date + timedelta(days=15)).replace(day=1)
            else:
                start_date = date
                end_date = date + timedelta(days=1)

            expenses = Expenses.objects.filter(user=request.user, date__range=[start_date, end_date])

        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        categories_summary = (
            ExpenseCategories.objects.filter(expense__in=expenses)
            .values("category__name")
            .annotate(total_amount=Sum("expense__amount"))
            .order_by("category__name")
        )

        # Sum expenses by date
        expense_data = expenses.values('date').annotate(total_amount=Sum('amount')).order_by('date')

        response_data = {
            'expenses': [{'x': item['date'], 'y': item['total_amount']} for item in expense_data],
            'total_expense': total_expense,
            'categories_summary': [
                {
                    "category": category["category__name"],
                    "total_amount": category["total_amount"],
                }
                for category in categories_summary
            ]
        }

        return Response(response_data)
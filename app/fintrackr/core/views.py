from datetime import datetime
from rest_framework import generics, permissions, status, viewsets
from django.db.models import Sum 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Users, Incomes, Categories, Expenses, ExpenseCategories
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UpdateUserSerializer,
    IncomeSerializer,
    CategorySerializer,
    ExpenseSerializer,
)


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
    
class IncomeListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        filters = {"user": request.user}

        try: 
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                filters["date__gte"] = start_date

            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                filters["date__lte"] = end_date
        
        except ValueError:
            return Response(
                {"error": "Dates must be in the format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        incomes = Incomes.objects.filter(**filters)
        serializer = IncomeSerializer(incomes, many = True)

        return Response(serializer.data, status=status.HTTP_200_OK)

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
            return Response({"error": "Income not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = IncomeSerializer(income)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, income_id):
        income = self.get_object(income_id, request.user)
        if income is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = IncomeSerializer(income, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, income_id):
        income = self.get_object(income_id, request.user)
        if income is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        income.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IncomeSourceSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Aggregate incomes by source for the authenticated user
        source_summary = (
            Incomes.objects
            .filter(user=request.user)  # Filter by the current user
            .values('source')  # Group by source
            .annotate(total_amount=Sum('amount'))  # Sum amounts for each source
            .order_by('source')  # Optional: order by source
        )

        # Format the response data
        response_data = [
            {
                "source": income["source"],
                "total_amount": income["total_amount"]
            }
            for income in source_summary
        ]

        return Response(response_data, status=status.HTTP_200_OK)


class ExpenseListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        filters = {"user": request.user}

        try: 
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                filters["date__gte"] = start_date

            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                filters["date__lte"] = end_date
        
        except ValueError:
            return Response(
                {"error": "Dates must be in the format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        expenses = Expenses.objects.filter(**filters)
        serializer = ExpenseSerializer(expenses, many = True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

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
            return Response({"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, expense_id):
        expense = self.get_object(expense_id, request.user)
        if not expense:
            return Response({"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, expense_id):
        expense = self.get_object(expense_id, request.user)
        if not expense:
            return Response({"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        expense.delete()
        return Response({"message": "Expense deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # Make this view publicly accessible


class ExpenseCategorySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        try: 
            filters = {"expense__user": request.user}

            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                filters["expense__date__gte"] = start_date

            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                filters["expense__date__lte"] = end_date
        
        except ValueError:
            return Response(
                {"error": "Dates must be in the format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        categories_summary = (
            ExpenseCategories.objects
            .filter(**filters)
            .values('category__name')
            .annotate(total_amount=Sum('expense__amount'))
            .order_by('category__name')
        )

        response_data = [
            {
                "category": category["category__name"],
                "total_amount": category["total_amount"]
            }
            for category in categories_summary
        ]

        return Response(response_data, status=status.HTTP_200_OK)
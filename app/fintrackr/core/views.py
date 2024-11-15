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
            return Incomes.objects.get(income_id=income_id, user=user)
        except Incomes.DoesNotExist:
            return None

    def get(self, request, income_id):
        income = self.get_object(income_id, request.user)
        if income is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = IncomeSerializer(income)
        return Response(serializer.data)

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

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # Make this view publicly accessible


 

class ExpenseCategorySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Aggregate expenses by category for the authenticated user
        categories_summary = (
            ExpenseCategories.objects
            .filter(expense__user=request.user)  # Filter by the current user
            .values('category__name')  # Group by category name
            .annotate(total_amount=Sum('expense__amount'))  # Sum the amount of related expenses
            .order_by('category__name')  # Order by category name (optional)
        )

        # Format the response data
        response_data = [
            {
                "category": category["category__name"],
                "total_amount": category["total_amount"]
            }
            for category in categories_summary
        ]

        return Response(response_data, status=status.HTTP_200_OK)
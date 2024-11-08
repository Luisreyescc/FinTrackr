from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from fintrackr.core.models import Users


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            if Users.objects.filter(email=serializer.validated_data["email"]).exists():
                return Response(
                    {"error": "Email is already registered"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if Users.objects.filter(
                user_name=serializer.validated_data["user_name"]
            ).exists():
                return Response(
                    {"error": "Username already taken"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                serializer.save()
                return Response(
                    {"message": "User successfully created"},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"error": f"An unexpected error occurred: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = Users.objects.get(user_name=username)
            if check_password(password, user.password_hash):
                return Response(
                    {"message": "Login successful"}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except Users.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

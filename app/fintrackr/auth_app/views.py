import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from datetime import datetime


class RegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("user_name")
        password = request.data.get("password_hash")
        name = request.data.get("name")
        last_name = request.data.get("last_name")
        phone = request.data.get("phone")
        curp = request.data.get("curp")
        rfc = request.data.get("rfc")
        birth_date = request.data.get("birth_date")

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email is already registered"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        user_data = {
            "user_name": username,
            "email": email,
            "password_hash": password,
            "name": name,
            "last_name": last_name,
            "phone": phone,
            "curp": curp,
            "rfc": rfc,
            "birth_date": birth_date,
        }

        try:
            response = requests.post("http://localhost:8000/api/users/", json=user_data)
            if response.status_code == 201:
                return Response(
                    {"message": "User successfully created"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "Failed to create user on external API"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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

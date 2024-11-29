from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from core.models import Users
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SendCodeSerializer, ValidateCodeSerializer, ChangePasswordSerializer
import random

RECOVERY_CODES = {}

class SendCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data["user_name"]
            email = serializer.validated_data["email"]
            try:
                user = Users.objects.get(user_name=user_name, email=email)
                code = str(random.randint(100000, 999999)) 
                RECOVERY_CODES[user.user_name] = code
                send_mail(
                    subject="Password Recovery Code",
                    message=f"Your recovery code is {code}",
                    from_email=None,
                    recipient_list=[email],
                )
                return Response({"message": "Recovery code sent successfully."}, status=status.HTTP_200_OK)
            except Users.DoesNotExist:
                return Response({"error": "User with provided details not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ValidateCodeSerializer(data=request.data)
        if serializer.is_valid():
            recovery_code = serializer.validated_data["recovery_code"]
            user_name = serializer.validated_data["user_name"]
            if user_name in RECOVERY_CODES and RECOVERY_CODES[user_name] == recovery_code:
                return Response({"message": "Code validated successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid recovery code."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import logging

logger = logging.getLogger(__name__)

class ChangePasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info(f"Received data: {request.data}")
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user_name = request.data.get("user_name")
            if user_name in RECOVERY_CODES:  # Ensure user validated the code
                try:
                    user = Users.objects.get(user_name=user_name)
                    logger.info(f"Changing password for user: {user_name}")
                    user.set_password(serializer.validated_data["password"])
                    user.save()
                    del RECOVERY_CODES[user_name]  # Remove code after success
                    return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
                except Users.DoesNotExist:
                    logger.error(f"User not found: {user_name}")
                    return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            logger.error(f"No validated recovery code found for user: {user_name}")
            return Response({"error": "No validated recovery code found for user."}, status=status.HTTP_400_BAD_REQUEST)
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
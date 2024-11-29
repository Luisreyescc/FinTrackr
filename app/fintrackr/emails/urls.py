from django.urls import path
from .views import SendCodeView, ValidateCodeView, ChangePasswordView

urlpatterns = [
    path("send-code/", SendCodeView.as_view(), name="send-code"),
    path("validate-code/", ValidateCodeView.as_view(), name="validate-code"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]

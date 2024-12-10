from django.urls import path
from .views import SendCodeView, ValidateCodeView, ChangePasswordView, IncomeExpensePDFView

urlpatterns = [
    path("send-code/", SendCodeView.as_view(), name="send-code"),
    path("validate-code/", ValidateCodeView.as_view(), name="validate-code"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),

    #pdf view
    path("pdf/", IncomeExpensePDFView.as_view(), name="send-pdf"),
]

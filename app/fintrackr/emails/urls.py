from django.urls import path
from .views import SendCodeView, ValidateCodeView, ChangePasswordView, SendCodeSignView, RegisterView, ValidateCodeSignView, IncomeExpensePDFView

urlpatterns = [
    # Recovery password views
    path("send-code/", SendCodeView.as_view(), name="send-code"),
    path("validate-code/", ValidateCodeView.as_view(), name="validate-code"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    # Register views
    path("send-code-sign/", SendCodeSignView.as_view(), name="send-code-sign"),
    path("validate-code-sign/", ValidateCodeSignView.as_view(), name="validate-code-sign"),
    path("register/", RegisterView.as_view(), name="register"),

    #pdf view
    path("pdf/", IncomeExpensePDFView.as_view(), name="send-pdf"),
]

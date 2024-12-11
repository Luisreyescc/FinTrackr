from django.urls import path
from .views import CheckUserEmailAssociationView, SendCodeView, ValidateCodeView, ChangePasswordView, CheckAvailabilityView, SendCodeSignView, RegisterView, ValidateCodeSignView, IncomeExpensePDFView

urlpatterns = [
    # Recovery password views
    path("check-user-email-association/", CheckUserEmailAssociationView.as_view(), name="check-user-email-association"),
    path("send-code/", SendCodeView.as_view(), name="send-code"),
    path("validate-code/", ValidateCodeView.as_view(), name="validate-code"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    # Register views
    path("check-availability/", CheckAvailabilityView.as_view(), name="check-availability"),
    path("send-code-sign/", SendCodeSignView.as_view(), name="send-code-sign"),
    path("validate-code-sign/", ValidateCodeSignView.as_view(), name="validate-code-sign"),
    path("register/", RegisterView.as_view(), name="register"),

    #pdf view
    path("pdf/", IncomeExpensePDFView.as_view(), name="send-pdf"),
]

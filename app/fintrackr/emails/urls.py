from django.urls import path
from .views import SendCodeView, ValidateCodeView, ChangePasswordView
from .pdfView import start_email_task, stop_email_task

urlpatterns = [
    path("send-code/", SendCodeView.as_view(), name="send-code"),
    path("validate-code/", ValidateCodeView.as_view(), name="validate-code"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),

    #pdf view
    path("start-thread/", start_email_task, name="start-thread"), 
    path("stop-thread/", stop_email_task, name="stop-thread"),
]

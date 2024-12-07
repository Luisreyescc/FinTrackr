from django.urls import path
from .views import SendCodeView, ValidateCodeView, ChangePasswordView
from .pdfView import start_thread, stop_thread

urlpatterns = [
    path("send-code/", SendCodeView.as_view(), name="send-code"),
    path("validate-code/", ValidateCodeView.as_view(), name="validate-code"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),

    #pdf view
    path("start-thread/", start_thread, name="start-thread"), 
    path("stop-thread/", stop_thread, name="stop-thread"),
]

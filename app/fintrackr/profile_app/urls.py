from django.urls import path
from .views import ProfileEditView

urlpatterns = [
    path('update/', ProfileEditView.as_view(), name='update_user'),
]
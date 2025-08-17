from django.urls import path
from .views import RegistrationAPIVeiw


urlpatterns = [
    path("signup/", RegistrationAPIVeiw.as_view(), name="signup-user")
]

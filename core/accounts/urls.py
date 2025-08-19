from django.urls import path
from .views import RegistrationAPIVeiw, CustomTokenObtainPairView, ChangePasswordApiView, ProfileApiView


urlpatterns = [
    path("signup/", RegistrationAPIVeiw.as_view(), name="signup-user"),
    path("token/create/", CustomTokenObtainPairView.as_view()),





    path("password/change/", ChangePasswordApiView.as_view()),
    path("profile/", ProfileApiView.as_view())
]

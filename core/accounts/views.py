from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import CustomUser, Profile
from .serializers import (
    RegistrationSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView
from django.core.mail import send_mail
from .utils.send_email import EmailThread
from rest_framework.views import APIView
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.conf import settings
import jwt


class RegistrationAPIVeiw(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {"email": serializer.validated_data["email"]}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    model = CustomUser
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class TestEmailSend(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        email_obj = send_mail(
            "subject here",
            "Send Node :)",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )

        EmailThread(email_obj).start()

        return Response("email sent")


class ActivationApiView(APIView):

    def get(self, request, *args, **kwargs):
        token = request.query_params.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activation link has expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.InvalidTokenError:
            return Response(
                {"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST
            )
        user_obj = CustomUser.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response(
                {"error": "Account is already activated"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"detail": "Account activated successfully"}, status=status.HTTP_200_OK
        )

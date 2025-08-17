from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import CustomUser, Profile
from .serializers import RegistrationSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny



    


class RegistrationAPIVeiw(generics.GenericAPIView):
    serializer_class = RegistrationSerializer


    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "email":serializer.validated_data["email"]
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
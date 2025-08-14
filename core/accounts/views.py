from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import CustomUser, Profile
from .serializers import ProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny


@api_view(["GET"])
def user_lists(request):
    queryset = Profile.objects.all()
    serializer = ProfileSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)





@api_view(["GET"])
def user_profile(request, id):
    try:
        user = Profile.objects.get(id=id) 
    except Profile.DoesNotExist:
        return Response({"detail":"item does not exis"},status=status.HTTP_404_NOT_FOUND)
    serializer = ProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)






api_view(["PUT", "PATCH"])
def profiledetail(request, id):
    profile = get_object_or_404(Profile,pk=id,status=True)
    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    



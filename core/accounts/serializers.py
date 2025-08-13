from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import Profile, CustomUser




class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "id", "created_date"]





class ProfileSerializer(ModelSerializer):
    user = SlugRelatedField(queryset=CustomUser.objects.all(), slug_field = "last_name")
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "image",
                "date_created" ,"bio", "last_login", "user"]

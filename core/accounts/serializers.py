from rest_framework.serializers import ModelSerializer, SlugRelatedField
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from .models import Profile, CustomUser




class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "created_date", "password", "password1"]



    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError("Passwords do not match!")
        
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password":list(e.messages)})

        return super().validate(attrs)


    def create(self, validated_data):
        validated_data.pop("password1", None)    
        return CustomUser.objects.create_user(**validated_data)    
    
    


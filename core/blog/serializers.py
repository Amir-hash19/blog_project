from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post, Category
from accounts.models import CustomUser, Profile




class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field ="name")
    class Meta:
        model = Post
        fields = ["image", "title", "author", "content",
                "status", "category", "created_at", "updated_date",
                "published_date"]
        
    def get_author(self, obj):
        try:
            profile = Profile.objects.get(user=obj.author)
            return f"{profile.first_name} {profile.last_name}"
        except Profile.DoesNotExist:
            return obj.author.email




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
        
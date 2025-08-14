from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post, Category
from accounts.models import CustomUser, Profile
from django.urls import reverse




class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field ="name")
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ["image", "title", "author", "content","snippet","relative_url",
                "status", "category", "created_at", "updated_date",
                "published_date", "absolute_url"]
        
    def get_author(self, obj):
        try:
            profile = Profile.objects.get(user=obj.author)
            return f"{profile.first_name} {profile.last_name}"
        except Profile.DoesNotExist:
            return obj.author.email


    def get_absolute_url(self, obj):
        request = self.context.get("request")
        relative_url = reverse("post-detail", kwargs={"pk": obj.pk})
        if request:
            return request.build_absolute_uri(relative_url)
        return relative_url




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

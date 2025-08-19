from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post, Category
from accounts.models import CustomUser, Profile
from django.urls import reverse


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="name"
    )
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField()
    author_email = serializers.EmailField(source="author.email", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "image",
            "title",
            "author",
            "content",
            "snippet",
            "relative_url",
            "status",
            "category",
            "created_at",
            "updated_date",
            "published_date",
            "absolute_url",
            "author_email",
        ]

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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        parser_context = getattr(request, "parser_context", {}) if request else {}
        kwargs = parser_context.get("kwargs", {})

        if kwargs.get("pk"):
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("content", None)
        rep["category"] = CategorySerializer(instance.category).data
        return rep

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

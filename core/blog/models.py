from django.db import models
from accounts.models import CustomUser


class Post(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=250)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title



class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
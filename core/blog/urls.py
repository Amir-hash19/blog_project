from django.urls import path
from .views import PostViewset



urlpatterns = [
    path("post/", PostViewset.as_view({"get":"list", "post":"create"}), name="post-list"),
    path("post/<int:pk>/", PostViewset.as_view({"get":"retrieve", "put":"update", "patch":"partial_update", "delete":"destroy"}), name="detail-list"),

]

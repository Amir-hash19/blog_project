from django.urls import path, include
from .views import PostViewset, CategoryModelViewSet, PostModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('post', PostModelViewSet, basename='post')
router.register('category', CategoryModelViewSet, basename='category')



urlpatterns = [
    # path("post/", PostViewset.as_view({"get":"list", "post":"create"}), name="post-list"),
    # path("post/<int:pk>/", PostViewset.as_view({"get":"retrieve", "put":"update", "patch":"partial_update", "delete":"destroy"}), name="detail-list"),
    path('', include(router.urls))
]

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination


class PostViewset(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        post_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post_object)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        post_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post_object, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

    def partial_update(self, request, pk=None):
        post_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post_object, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post_object = get_object_or_404(self.queryset, pk=pk)
        post_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly
                        ]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()



class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["=title", "content"]
    filterset_fields = ["category", "author", "status"]
    ordering_fields = ["published_date"]
    ordering = ["-published_date"] 
    pagination_class = DefaultPagination
    queryset = Post.objects.all()






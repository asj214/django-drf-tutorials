from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer, PostCommentSerializer
from comments.models import Comment


class PostViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticatedOrReadOnly]
  serializer_class = PostSerializer
  queryset = Post.objects.prefetch_related('user').all()

  def get_queryset(self):
    return self.queryset
    
  def get_object(self, pk=None):
    try:
      return self.queryset.get(pk=pk)
    except Post.DoesNotExist:
      raise NotFound('Not Found')
    
  def list(self, request, *args, **kwargs):
    page = self.paginate_queryset(self.get_queryset())
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)
    
  def create(self, request, *args, **kwargs):
    context = {
      'user': request.user,
    }
    serializer = self.serializer_class(
      data=request.data,
      context=context,
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)
    
  def retrieve(self, request, pk=None, *args, **kwargs):
    post = self.get_object(pk)
    serializer = self.serializer_class(post)

    return Response(serializer.data)
    
  def update(self, request, pk=None, *args, **kwargs):
    post = self.get_object(pk)
    serializer = self.serializer_class(
      post,
      data=request.data,
      context={'user': request.user},
      partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)
    
  def destroy(self, request, pk=None, *args, **kwargs):
    post = self.get_object(pk)
    post.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


class PostCommentViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticatedOrReadOnly]
  serializer_class = PostCommentSerializer
  queryset = Comment.objects.prefetch_related('user').all()

  def get_post_queryset(self, post_id=None):
    try:
      post = Post.objects.get(pk=post_id)
      return post.comments.all()
    except Post.DoesNotExist:
      raise NotFound('Not Found')

  def get_queryset(self):
    return self.queryset

  def get_object(self, pk=None):
    try:
      return self.queryset.get(pk=pk)
    except Comment.DoesNotExist:
      raise NotFound('Not Found')
  
  def list(self, request, post_id, *args, **kwargs):
    page = self.paginate_queryset(self.get_post_queryset(post_id))
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)

  def create(self, request, post_id, *args, **kwargs):
    context = {
      'user': request.user,
      'post_id': post_id
    }
    serializer = self.serializer_class(
      data=request.data,
      context=context,
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def update(self, request, post_id=None, pk=None, *args, **kwargs):
    comment = self.get_object(pk)
    serializer = self.serializer_class(
      comment,
      data=request.data,
      context={'user': request.user},
      partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)
    
  def destroy(self, request, post_id=None, pk=None, *args, **kwargs):
    comment = self.get_object(pk)
    comment.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)
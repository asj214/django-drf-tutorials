from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticatedOrReadOnly]
  serializer_class = CommentSerializer
  queryset = Comment.objects.prefetch_related('user').all()

  def get_queryset(self):
    return self.queryset

  def get_object(self, pk=None):
    try:
      return self.queryset.get(pk=pk)
    except Comment.DoesNotExist:
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

  def update(self, request, pk=None, *args, **kwargs):
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
    
  def destroy(self, request, pk=None, *args, **kwargs):
    comment = self.get_object(pk)
    comment.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)
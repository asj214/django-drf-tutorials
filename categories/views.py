from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticatedOrReadOnly]
  serializer_class = CategorySerializer
  queryset = Category.objects.all()

  def get_queryset(self):
    return self.queryset
    
  def get_object(self, pk=None):
    try:
      return self.queryset.prefetch_related('user').get(pk=pk)
    except Category.DoesNotExist:
      raise NotFound('Not Found')

  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = self.get_serializer()
    res = serializer.generate_categories(queryset)

    return Response(res)

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
    category = self.get_object(pk)
    serializer = self.serializer_class(category)

    return Response(serializer.data)
    
  def update(self, request, pk=None, *args, **kwargs):
    category = self.get_object(pk)
    serializer = self.serializer_class(
      category,
      data=request.data,
      context={'user': request.user},
      partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)
    
  def destroy(self, request, pk=None, *args, **kwargs):
    category = self.get_object(pk)
    category.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)
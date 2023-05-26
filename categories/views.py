from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Category
from .serializers import CategorySerializer
from products.models import Product
from products.serializers import ProductSerializer


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
  

class CategoryProductList(generics.ListCreateAPIView):
  permission_classes = [AllowAny]
  serializer_class = ProductSerializer
  queryset = Product.objects.prefetch_related('categories', 'user').all()

  def get_queryset(self, category_id):
    qs = self.queryset
    category = Category.objects.get(id=category_id)
    qs = qs.filter(categories__id__in=category.path)

    return qs

  def list(self, request, category_id, *args, **kwargs):
    page = self.paginate_queryset(self.get_queryset(category_id))
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)
  
from django.db import IntegrityError, transaction
from rest_framework import serializers
from users.serializers import UserSerializer
from categories.models import Category
from categories.serializers import CategoryRelationSerializer
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  category_ids = serializers.ListField(
    child=serializers.IntegerField(),
    write_only=True
  )
  categories = CategoryRelationSerializer(read_only=True, many=True)
  name = serializers.CharField(max_length=200)
  price = serializers.DecimalField(max_digits=10, decimal_places=2)
  description = serializers.CharField()
  is_published = serializers.BooleanField(default=False, required=False)

  class Meta:
    model = Product
    fields = (
      'id',
      'user',
      'name',
      'price',
      'description',
      'is_published',
      'categories',
      'category_ids',
      'created_at',
      'updated_at'
    )
  
  def create(self, validated_data):
    user = self.context.pop('user')
    category_ids = validated_data.pop('category_ids', [])

    try:
      with transaction.atomic():
        product = Product.objects.create(
          user=user,
          **validated_data
        )
        categories = Category.objects.filter(id__in=category_ids).all()
        product.categories.add(*categories)

        return product

    except IntegrityError:
      raise Exception("Something went wrong")

  def update(self, instance, validated_data):
    category_ids = validated_data.pop('category_ids', [])
    try:
      with transaction.atomic():
        for (key, value) in validated_data.items():
          setattr(instance, key, value)
        instance.save()

        categories = Category.objects.filter(id__in=category_ids).all()
        instance.categories.clear()
        instance.categories.add(*categories)
        return instance
    except IntegrityError:
      raise Exception("Something went wrong")


class ProductRelateSerializer(serializers.ModelSerializer):
  categories = CategoryRelationSerializer(read_only=True, many=True)

  class Meta:
    model = Product
    fields = (
      'id',
      'name',
      'price',
      'description',
      'is_published',
      'categories',
      'created_at',
      'updated_at'
    )
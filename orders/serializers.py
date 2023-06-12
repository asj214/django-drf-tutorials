from rest_framework import serializers
from users.serializers import UserSerializer
from products.serializers import ProductSerializer
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  name = serializers.CharField(max_length=200)
  price = serializers.DecimalField(max_digits=10, decimal_places=2)
  products = ProductSerializer(read_only=True, many=True)
  product_ids = serializers.ListField(
    child=serializers.IntegerField(),
    write_only=True
  )

  class Meta:
    model = Order
    fields = (
      'id',
      'user',
      'name',
      'price',
      'status',
      'products',
      'product_ids',
      'delivery_started_at',
      'delivery_finished_at',      
      'created_at',
      'updated_at'
    )
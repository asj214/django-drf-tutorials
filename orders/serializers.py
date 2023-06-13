from rest_framework import serializers
from users.serializers import UserSerializer
from products.models import Product
from products.serializers import ProductRelateSerializer
from .models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
  name = serializers.CharField(max_length=200)
  price = serializers.DecimalField(max_digits=10, decimal_places=2)
  qty = serializers.IntegerField()
  status = serializers.CharField(max_length=200)

  class Meta:
    model = OrderProduct
    fields = (
      'id',
      'name',
      'price',
      'qty',
      'status',
      'delivery_started_at',
      'delivery_finished_at',      
      'created_at',
      'updated_at'
    )


class OrderCartSerializer(serializers.Serializer):
  id = serializers.IntegerField()
  qty = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):
  cart = serializers.ListField(
    child=OrderCartSerializer(),
    write_only=True
  )
  amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
  # user = UserSerializer(read_only=True)
  order_products = OrderProductSerializer(read_only=True, many=True)

  class Meta:
    model = Order
    fields = (
      'id',
      # 'user',
      'amount',
      'status',
      'cart',
      'order_products',
      'created_at',
      'updated_at'
    )
  
  def create(self, validated_data):
    user = self.context.pop('user')
    cart = validated_data.pop('cart', [])

    products = Product.objects.filter(
      id__in=[c.get('id') for c in cart]
    ).all()
    amount = sum(p.price * c['qty'] for p, c in zip(products, cart))

    order = Order.objects.create(
      user=user,
      amount=amount,
      **validated_data
    )

    for p, c in zip(products, cart):
      order.orderproduct_set.create(
        product=p,
        name=p.name,
        price=p.price,
        qty=c.get('qty', 1)
      )

    return order



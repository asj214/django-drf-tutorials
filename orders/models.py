from django.db import models
from conf.models import BaseModel, SoftDeleteModel


ORDER_STATUS_CHOICES = (
  ('ORDER.NONE', '대기'),
  ('PAYMENT.WAIT', '결제대기'),
  ('PAYMENT.COMPLETE', '결제완료'),
  ('ORDER.CANCEL', '주문취소'),
  ('ORDER.SOLDOUT', '품절')
)

ORDER_PRODUCT_STATUS_CHOICES = (
  ('ORDER.NONE', '대기'),
  ('DELIVERY.WAIT', '배송준비중'),
  ('DELIVERY.IN', '배송중'),
  ('DELIVERY.COMPLETE', '배송완료'),
  ('PRODUCT.SOLDOUT', '품절')
)


class Order(BaseModel, SoftDeleteModel):
  user = models.ForeignKey(
    'users.User',
    on_delete=models.DO_NOTHING,
    db_constraint=False,
    default=None,
    null=True,
    related_name='orders'
  )

  products = models.ManyToManyField(
    'products.Product',
    through='OrderProduct',
    related_name='orders'
  )

  amount = models.DecimalField('총 주문 가격', max_digits=10, decimal_places=2)
  status = models.CharField('주문 상태', max_length=45, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

  class Meta:
    db_table = 'orders'
    ordering = ['-id']
    indexes = []
  
  def __str__(self):
    return '{}'.format(self.id)


class OrderProduct(BaseModel, SoftDeleteModel):
  order = models.ForeignKey(
    Order,
    on_delete=models.DO_NOTHING,
    db_constraint=False
  )

  product = models.ForeignKey('products.Product',
    on_delete=models.DO_NOTHING,
    db_constraint=False,
  )

  name = models.CharField('주문 당시 상품명', max_length=200)
  price = models.DecimalField('주문 당시 상품가격', max_digits=10, decimal_places=2, default=0)
  qty = models.PositiveIntegerField(default=0)

  status = models.CharField('주문 상태', max_length=45, choices=ORDER_PRODUCT_STATUS_CHOICES, default=ORDER_PRODUCT_STATUS_CHOICES[0][0])
  delivery_started_at = models.DateTimeField('배송시작일', null=True, default=None)
  delivery_finished_at = models.DateTimeField('배송종료일', null=True, default=None)

  class Meta:
    db_table = 'order_products'
    ordering = ['-id']
    indexes = []
  
  def __str__(self):
    return '{}'.format(self.id)
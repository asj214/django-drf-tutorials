from django.db import models
from conf.models import BaseModel, SoftDeleteModel


STATUS_CHOICES = (
  ('PAYMENT.WAIT', '결제대기'),
  ('PAYMENT.COMPLETE', '결제완료'),
  ('DELIVERY.WAIT', '배송준비중'),
  ('DELIVERY.IN', '배송중'),
  ('DELIVERY.COMPLETE', '배송완료'),
  ('ORDER.CANCEL', '주문취소'),
  ('ORDER.SOLDOUT', '품절')
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

  name = models.CharField('주문 당시 상품명', max_length=200)
  price = models.DecimalField('주문 당시 상품가격', max_digits=10, decimal_places=2)
  status = models.CharField('주문 상태', max_length=45, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

  delivery_started_at = models.DateTimeField('배송시작일', null=True, default=None)
  delivery_finished_at = models.DateTimeField('배송종료일', null=True, default=None)

  product = models.ManyToManyField(
    'products.Product',
    db_constraint=False,
    related_name='orders'
  )

  class Meta:
    db_table = 'orders'
    ordering = ['-id']
    indexes = []
  
  def __str__(self):
    return '{}'.format(self.id)

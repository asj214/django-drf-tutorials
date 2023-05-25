from django.db import models
from conf.models import BaseModel, SoftDeleteModel


class Product(BaseModel, SoftDeleteModel):
  user = models.ForeignKey(
    'users.User',
    on_delete=models.DO_NOTHING,
    db_constraint=False,
    default=None,
    null=True,
    related_name='products'
  )
  name = models.CharField('상품명', max_length=200)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField('상품 설명')

  categories = models.ManyToManyField(
    'categories.Category',
    on_delete=models.DO_NOTHING,
    db_constraint=False,
    related_name='products'
  )

  class Meta:
    db_table = 'products'
    ordering = ['-id']
    indexes = []
  
  def __str__(self):
    return f'{self.id}'
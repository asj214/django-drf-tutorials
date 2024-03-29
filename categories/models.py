from django.db import models
from conf.models import BaseModel, SoftDeleteModel


class Category(BaseModel, SoftDeleteModel):
  parent = models.ForeignKey(
    'self',
    null=True,
    blank=True,
    on_delete=models.DO_NOTHING,
    db_constraint=False,
    related_name='children'
  )
  name = models.CharField('카테고리명', max_length=200)
  depth = models.IntegerField(default=0)
  user = models.ForeignKey(
    'users.User',
    on_delete=models.DO_NOTHING,
    db_constraint=False,
    default=None,
    null=True,
    related_name='categories'
  )
  path = models.JSONField(default=list)
  order = models.IntegerField('순서', default=0)
  is_published = models.BooleanField('공개 여부', default=False, db_index=True)

  product = models.ManyToManyField(
    'products.Product',
    db_constraint=False,
    related_name='categories'
  )

  def get_children_ids(self):
    ret = [self.id]
    for c in self.__class__.objects.filter(parent_id=self.id).all():
      ret = ret + c.get_children_ids()

    return ret

  class Meta:
    db_table = 'categories'
    ordering = ['parent__id', 'order']
    indexes = []
  
  def __str__(self):
    return '{}: {}'.format(self.id, self.name)
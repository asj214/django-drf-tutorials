from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from conf.models import BaseModel, SoftDeleteModel


class Comment(BaseModel, SoftDeleteModel):
  commentable_type = models.ForeignKey(
    ContentType,
    on_delete=models.DO_NOTHING,
    db_constraint=False,
  )
  commentable_id = models.PositiveIntegerField() 
  commentable = GenericForeignKey('commentable_type', 'commentable_id')

  user = models.ForeignKey(
    'users.User',
    on_delete=models.DO_NOTHING,
    db_constraint=False,
    default=None,
    null=True,
    related_name='comments'
  )
  body = models.TextField('본문')

  class Meta:
    db_table = 'comments'
    ordering = ['-id']
    indexes = []
  
  def __str__(self):
    return f'{self.id}'

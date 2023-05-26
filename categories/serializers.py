from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  name = serializers.CharField(max_length=200)
  order = serializers.IntegerField(default=0, required=False)
  is_published = serializers.BooleanField(default=False, required=False)

  class Meta:
    model = Category
    fields = (
      'id',
      'parent',
      'user',
      'name',
      'depth',
      'order',
      'is_published',
      'created_at',
      'updated_at'
    )

  def create(self, validated_data):
    user = self.context.pop('user')
    return Category.objects.create(
      user=user,
      **validated_data
    )

  def update(self, instance, validated_data):
    for (key, value) in validated_data.items():
      setattr(instance, key, value)

    instance.save()
    return instance

  def generate_categories(self, rows: list, parent_id=None, depth=0):
    ret = []
    for r in rows:
      if r.depth != depth or parent_id != r.parent_id:
        continue

      ret.append({
        'id': r.id,
        'parent_id': r.parent_id,
        'name': r.name,
        'depth': r.depth,
        'order': r.order,
        'is_published': r.is_published,
        'children': self.generate_categories(rows, parent_id=r.id, depth=depth+1)
      })

    return ret


class CategoryRelationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = (
      'id',
      'parent',
      'name',
      # 'depth',
      # 'order',
      # 'is_published',
    )
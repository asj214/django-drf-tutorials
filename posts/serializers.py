from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  title = serializers.CharField(max_length=200)
  body = serializers.CharField()

  class Meta:
    model = Post
    fields = (
      'id',
      'user',
      'title',
      'body',
      'created_at',
      'updated_at'
    )
  
  def create(self, validated_data):
    user = self.context.pop('user')
    return Post.objects.create(
      user=user,
      **validated_data
    )

  def update(self, instance, validated_data):
    for (key, value) in validated_data.items():
      setattr(instance, key, value)

    instance.save()
    return instance

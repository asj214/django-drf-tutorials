from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Post
from comments.models import Comment


class PostCommentSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  body = serializers.CharField()

  class Meta:
    model = Comment
    fields = (
      'id',
      'user',
      'body',
      'created_at',
      'updated_at'
    )

  def create(self, validated_data):
    post_id = self.context.pop('post_id')
    user = self.context.pop('user')

    post = Post.objects.get(pk=post_id)
    return post.comments.create(
      user=user,
      **validated_data
    )


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
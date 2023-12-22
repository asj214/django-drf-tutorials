from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
  commentable_id = serializers.IntegerField(write_only=True)
  commentable_type = serializers.CharField(write_only=True)
  user = UserSerializer(read_only=True)
  body = serializers.CharField()

  class Meta:
    model = Comment
    fields = (
      'id',
      'commentable_id',
      'commentable_type',
      'user',
      'body',
      'created_at',
      'updated_at'
    )

  def create(self, validated_data):
    user = self.context.pop('user')
    return Comment.objects.create(
      user=user,
      **validated_data
    )

  def update(self, instance, validated_data):
    for (key, value) in validated_data.items():
      setattr(instance, key, value)

    instance.save()
    return instance
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, PostCommentViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'posts', PostViewSet)

urlpatterns = [
  path(r'posts/<int:post_id>/comments', PostCommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
  })),
  path(r'posts/<int:post_id>/comments/<int:pk>', PostCommentViewSet.as_view({
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
  })),
]
urlpatterns += router.urls
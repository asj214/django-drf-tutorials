from rest_framework.routers import DefaultRouter
from .views import CommentViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'comments', CommentViewSet)

urlpatterns = []
urlpatterns += router.urls
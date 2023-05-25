from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryViewSet)

urlpatterns = []
urlpatterns += router.urls
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CategoryProductList


router = DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
  path(r'categories/<int:category_id>/products', CategoryProductList.as_view()),
]

urlpatterns += router.urls
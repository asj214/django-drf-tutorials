from django.contrib import admin
from django.urls import path, include


urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/', include('users.urls')),
  path('api/', include('posts.urls')),
  path('api/', include('comments.urls')),
  path('api/', include('categories.urls')),
  path('api/', include('products.urls')),
  path('api/', include('orders.urls')),
]

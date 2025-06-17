
from django.contrib import admin
from django.urls import path
from shop.views import ProductViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', ProductViewSet.as_view()),
]
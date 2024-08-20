from django.urls import path
from . import views

urlpatterns = [
    path('', views.load_product , name='products'),
    path('products/', views.load_product , name='products'),
    path('products/product_details/<int:id>',views.load_product_details , name='product_details')
]


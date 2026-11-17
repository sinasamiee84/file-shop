from django.urls import path
from apps.products.views import ProductListView, ProductDetailView, CategoryDetailView

app_name = 'products'

urlpatterns = [
    path('list/', ProductListView.as_view(), name='list'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'), # مسیر جدید برای مشاهده همه محصولات یک دسته
    path('<str:slug>/', ProductDetailView.as_view(), name='detail'),
]

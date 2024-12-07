from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, SliderImageViewSet

# router = DefaultRouter()
# router.register(r'category', CategoryViewSet, basename="category")
# router.register(r'product', ProductViewSet, basename="product")
# path('', include(router.urls)),
urlpatterns = [
    path('category/get-all/', CategoryViewSet.as_view({'get': 'list'}), name='category-list'),
    path('category/<slug:category_slug>/', CategoryViewSet.as_view({'get': 'retrieve'}), name='category-detail'),
   # path('category/<slug:category_slug>/product/', CategoryViewSet.as_view({'get': 'product_list'}), name='category-product-list'),
   path('product/get-by-category-slug/<slug:category_slug>/', CategoryViewSet.as_view({'get': 'product_list'}),name='product-list-by-category-slug'),
   path('category/<slug:category_slug>/product/<slug:product_slug>/', ProductViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
   path('slider-image/get-by-index/<int:index>/', SliderImageViewSet.as_view({'get': 'get_by_index'}), name='slider-image-by-index'),
]

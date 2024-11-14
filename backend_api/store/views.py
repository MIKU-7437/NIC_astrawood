from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
      Возвращает только категории

          Получение конкретной категории на основе слага(также отдает подкатегории).
          Возвращает:
              Category: Запрошенная категория.
    """
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        # Получаем все slug категорий, которые являются подкатегориями других категорий
        sub_category_slugs = Category.objects.filter(top_catgeory__isnull=False).values_list('slug', flat=True)
        # Фильтруем топ-категории (top_catgeory=None), исключая те, которые уже есть в подкатегориях
        queryset = Category.objects.filter(top_catgeory__isnull=True).exclude(slug__in=sub_category_slugs)
        return queryset

    def get_object(self):
        """
        Получение конкретной категории на основе слага.
        """
        category_slug = self.kwargs['category_slug']
        return get_object_or_404(Category, slug=category_slug)

    def get_all_products(self, category):
        """
        Получение всех продуктов из всех категорий и подкатегорий
        """
        products = Product.objects.filter(category=category, is_available=True)

        subcategories = Category.objects.filter(top_catgeory=category)

        for subcategory in subcategories:
            products = products | self.get_all_products(subcategory)

        return products

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category_slug', openapi.IN_PATH,
                description="Слаг категории",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: ProductSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def product_list(self, request, category_slug):
        """
        Получение продуктов из категории и всех её подкатегорий.
        Аргументы:
        category_slug (обязательный): слаг категории
        Ответ:
        Product (list): список продуктов из категорий и подкатегорий
        """
        category = self.get_object()
        products = self.get_all_products(category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
       Получение конкретного товара на основе предоставленного слага.
       Аргументы:
        category_slug (обязательный): слаг категории
        product_slug (обязательный): слаг продукта
       Возвращает:
           Product: Запрошенный товар.
    """
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category_slug', openapi.IN_PATH,
                description="Слаг категории",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'product_slug', openapi.IN_PATH,
                description="Слаг продукта",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: ProductSerializer()}
    )
    def get_object(self):
        """
        Получение конкретного товара на основе предоставленного слага.
        """
        product_slug = self.kwargs['product_slug']
        return get_object_or_404(Product, slug=product_slug)

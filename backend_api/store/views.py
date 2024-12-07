from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Category, Product, SliderImage
from .serializers import (CategorySerializer, ProductSerializer,
                          SliderImageSerializer)


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


class SliderImageViewSet(viewsets.ViewSet):
    """
    ViewSet для работы с изображениями слайдера.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'index', openapi.IN_PATH,
                description="Индекс изображения",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: SliderImageSerializer()}
    )
    @action(detail=False, methods=['get'], url_path='get-by-index/(?P<index>\\d+)')
    def get_by_index(self, request, index=None):
        """
        Возвращает изображение слайдера по его индексу.
        """
        try:
            index = int(index)
            slider_image = SliderImage.objects.all()[index]
        except (IndexError, ValueError):
            return Response({"detail": "Изображение с данным индексом не найдено."}, status=404)

        serializer = SliderImageSerializer(slider_image)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={200: SliderImageSerializer(many=True)}
    )
    def list(self, request):
        """
        Возвращает список всех изображений.
        """
        queryset = SliderImage.objects.all()
        serializer = SliderImageSerializer(queryset, many=True)
        return Response(serializer.data)

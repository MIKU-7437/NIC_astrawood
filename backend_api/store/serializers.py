from rest_framework import serializers

from .models import Category, Product, SliderImage


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'title',
            'slug',
            'description',
        ]

class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'title',
            'slug',
            'description',
            'sub_categories',
        ]
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'slug',
            'price',
            'is_available',
            'description',
            'stock',
            'category',
            'photo',
            'rating',
            'views',
        ]
        depth = 1


class SliderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderImage
        fields = ['id', 'photo']

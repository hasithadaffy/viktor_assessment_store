from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from .models import Book, MusicAlbum, SoftwareLicense, ShoppingCart, CartItem


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author",
                  "number_of_pages", "price", "weight"]


class MusicAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicAlbum
        fields = ["id", "artist", "title",
                  "number_of_tracks", "price", "weight"]


class SoftwareLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareLicense
        fields = ["id", "name", "price", "weight"]


class CartItemSerializer(serializers.ModelSerializer):
    product_type = serializers.SerializerMethodField()
    product_id = serializers.CharField(source="object_id", read_only=True)
    product_display = serializers.SerializerMethodField()
    unit_price = serializers.SerializerMethodField()
    unit_weight = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "quantity",
            "added_at",
            "product_type",
            "product_id",
            "product_display",
            "unit_price",
            "unit_weight",
        ]

    def get_product_type(self, obj: CartItem) -> str:
        return obj.content_type.model

    def get_product_display(self, obj: CartItem) -> str:
        return obj.product.get_display_name()

    def get_unit_price(self, obj: CartItem):
        return obj.product.price

    def get_unit_weight(self, obj: CartItem):
        return obj.product.weight


class ShoppingCartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.FloatField(read_only=True)
    total_weight = serializers.FloatField(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ["id", "created_at", "updated_at",
                  "items", "total_price", "total_weight"]

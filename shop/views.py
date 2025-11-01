from typing import Type

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from .models import Book, MusicAlbum, SoftwareLicense, ShoppingCart
from .serializers import (
    BookSerializer,
    MusicAlbumSerializer,
    SoftwareLicenseSerializer,
    ShoppingCartSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer


class MusicAlbumViewSet(viewsets.ModelViewSet):
    queryset = MusicAlbum.objects.all().order_by("id")
    serializer_class = MusicAlbumSerializer


class SoftwareLicenseViewSet(viewsets.ModelViewSet):
    queryset = SoftwareLicense.objects.all().order_by("id")
    serializer_class = SoftwareLicenseSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.prefetch_related(
        "items").all().order_by("id")
    serializer_class = ShoppingCartSerializer

    @action(detail=True, methods=["post"], url_path="add-item")
    def add_item(self, request, pk=None):
        """Body: {"model": "book|musicalbum|softwarelicense", "id": <int>, "quantity": <int>}
        """
        cart = self.get_object()
        model = request.data.get("model")
        obj_id = request.data.get("id")
        qty = int(request.data.get("quantity", 1))

        model_map: dict[str, Type] = {
            "book": Book,
            "musicalbum": MusicAlbum,
            "softwarelicense": SoftwareLicense,
        }
        if model not in model_map:
            return Response({"detail": "Invalid model."}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(model_map[model], pk=obj_id)
        cart.add(product, quantity=qty)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="remove-item")
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        model = request.data.get("model")
        obj_id = request.data.get("id")
        qty = int(request.data.get("quantity", 1))

        model_map: dict[str, Type] = {
            "book": Book,
            "musicalbum": MusicAlbum,
            "softwarelicense": SoftwareLicense,
        }
        if model not in model_map:
            return Response({"detail": "Invalid model."}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(model_map[model], pk=obj_id)
        cart.remove(product, quantity=qty)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="clear")
    def clear(self, request, pk=None):
        cart = self.get_object()
        cart.clear()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

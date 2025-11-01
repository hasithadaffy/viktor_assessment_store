from django.contrib import admin
from .models import Book, MusicAlbum, SoftwareLicense, ShoppingCart, CartItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "number_of_pages", "price", "weight")
    search_fields = ("title", "author")


@admin.register(MusicAlbum)
class MusicAlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist", "number_of_tracks", "price", "weight")
    search_fields = ("title", "artist")


@admin.register(SoftwareLicense)
class SoftwareLicenseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "weight")
    search_fields = ("name",)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("added_at",)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at", "total_price", "total_weight")
    inlines = [CartItemInline]

    def total_price(self, obj: ShoppingCart):
        return obj.total_price

    def total_weight(self, obj: ShoppingCart):
        return obj.total_weight
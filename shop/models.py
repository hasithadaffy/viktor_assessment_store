from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class BaseModel(models.Model):
    """Common fields for all models.

    Every product has an ID (pk) and a price in euros.
    Weight is optional because some models do not have a physical weight.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Book(BaseModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    number_of_pages = models.PositiveIntegerField()
    
    def get_display_name(self) -> str:
        return f"Book: {self.title} by {self.author}"
    

class MusicAlbum(BaseModel):
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    number_of_tracks = models.PositiveIntegerField()

    def get_display_name(self) -> str:
        return f"Album: {self.title} by {self.artist}"

    def __str__(self) -> str:
        return self.get_display_name()


class SoftwareLicense(BaseModel):
    name = models.CharField(max_length=255)

    def clean(self):
        if self.weight not in (None, 0):
            raise ValidationError("Software licenses must not have weight.")


class ShoppingCart(models.Model):
    """A simple cart container."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add(self, product: BaseModel, quantity: int = 1) -> "CartItem":
        if quantity < 1:
            raise ValidationError("Quantity must be positive.")
        ct = ContentType.objects.get_for_model(product)
        item, created = CartItem.objects.get_or_create(
            cart=self,
            content_type=ct,
            object_id=product.pk,
            defaults={"quantity": quantity},
        )
        if not created:
            item.quantity += quantity
            item.added_at = timezone.now()
            item.save(update_fields=["quantity", "added_at", "updated_at"])
        return item

    def remove(self, product: BaseModel, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValidationError("Quantity must be positive.")
        ct = ContentType.objects.get_for_model(product)
        try:
            item = CartItem.objects.get(cart=self, content_type=ct, object_id=product.pk)
        except CartItem.DoesNotExist:
            return
        if item.quantity <= quantity:
            item.delete()
        else:
            item.quantity -= quantity
            item.save(update_fields=["quantity", "updated_at"])

    def clear(self) -> None:
        self.items.all().delete()

    @property
    def total_price(self) -> float:
        total = 0
        for item in self.items.select_related("content_type"):
            prod = item.product
            total += float(item.quantity) * float(prod.price)
        return round(total, 2)

    @property
    def total_weight(self) -> float:
        total = 0
        for item in self.items.select_related("content_type"):
            prod = item.product
            weight = float(prod.weight) if prod.weight is not None else 0.0
            total += float(item.quantity) * weight
        return round(total, 3)

    def __str__(self) -> str:
        return f"Cart #{self.pk}"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cart = models.ForeignKey(ShoppingCart, related_name="items", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=36)
    product = GenericForeignKey("content_type", "object_id")
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ["added_at", "pk"]
        unique_together = (
            ("cart", "content_type", "object_id"),
        )

    def clean(self):
        if self.quantity < 1:
            raise ValidationError("Quantity must be positive.")

    def __str__(self) -> str:
        return f"{self.product} x {self.quantity}"
import decimal
from django.test import TestCase
from shop.models import ShoppingCart, Book, MusicAlbum, SoftwareLicense


class CartTests(TestCase):
    def setUp(self):
        self.book_a = Book.objects.create(
            title="A", author="Auth", number_of_pages=120,
            price=decimal.Decimal("10.00"), weight=decimal.Decimal("0.300"),
        )
        self.book_b = Book.objects.create(
            title="B", author="Auth", number_of_pages=200,
            price=decimal.Decimal("12.50"), weight=decimal.Decimal("0.450"),
        )
        self.album_c = MusicAlbum.objects.create(
            artist="Art", title="C", number_of_tracks=10,
            price=decimal.Decimal("9.99"), weight=decimal.Decimal("0.100"),
        )
        self.lic_d = SoftwareLicense.objects.create(
            name="Suite D", price=decimal.Decimal("49.00"),
        )

    def test_totals(self):
        cart = ShoppingCart.objects.create()
        cart.add(self.book_a, quantity=2)
        cart.add(self.album_c, quantity=1)
        cart.add(self.lic_d, quantity=3)

        self.assertEqual(cart.total_price, 2*10.00 + 9.99 + 3*49.00)
        self.assertEqual(cart.total_weight, round(2*0.300 + 0.100, 3))

    def test_remove(self):
        cart = ShoppingCart.objects.create()
        cart.add(self.book_b, quantity=2)
        cart.remove(self.book_b, quantity=1)
        self.assertEqual(cart.items.first().quantity, 1)
        cart.remove(self.book_b, quantity=1)
        self.assertEqual(cart.items.count(), 0)

    def test_recommendations(self):
        c1 = ShoppingCart.objects.create()
        c1.add(self.book_a)
        c1.add(self.book_b)
        c1.add(self.album_c)

        c2 = ShoppingCart.objects.create()
        c2.add(self.book_a)
        c2.add(self.book_b)

        c3 = ShoppingCart.objects.create()
        c3.add(self.book_a)
        c3.add(self.album_c)
        c3.add(self.book_b)
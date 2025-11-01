from django_filters import FilterSet
from .models import Book, MusicAlbum, SoftwareLicense

class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'author': ['exact', 'icontains'],
            'number_of_pages': ['exact', 'gte', 'lte'],
            'price': ['exact', 'gte', 'lte'],
            'weight': ['exact', 'gte', 'lte'],
        }

class MusicAlbumFilter(FilterSet):
    class Meta:
        model = MusicAlbum
        fields = {
            'artist': ['exact', 'icontains'],
            'title': ['exact', 'icontains'],
            'number_of_tracks': ['exact', 'gte', 'lte'],
            'price': ['exact', 'gte', 'lte'],
            'weight': ['exact', 'gte', 'lte'],
        }


class SoftwareLicenseFilter(FilterSet):
    class Meta:
        model = SoftwareLicense
        fields = {
            'name': ['exact', 'icontains'],
            'price': ['exact', 'gte', 'lte'],
            'weight': ['exact', 'gte', 'lte'],
        }
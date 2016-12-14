from main.models import Author, Book
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    def get_full_name(self, instance):
        return '{} {}'.format(instance.name, instance.surname)

    class Meta:
        model = Author
        fields = ('id', 'full_name', 'birth_date')


class BookSerializer(serializers.ModelSerializer):

    authors = AuthorSerializer(many=True)

    """
    authors = serializers.SerializerMethodField()

    def get_authors(self, instance):
        return [AuthorSerializer(a).data for a in instance.authors.all()]
    """

    class Meta:
        model = Book
        fields = ('id', 'title', 'authors', 'lc_classification')

from rest_framework import serializers
from bookAPI.models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book"""

    class Meta:
        model = Book
        fields = ('id', 'name', 'author')
        # 'published_on'


from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)


class FooSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta(object):
        model = Book
        fields = "__all__"
        # only necessary in DRF3
        list_serializer_class = BulkListSerializer


# class FooView(ListBulkCreateUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = FooSerializer


class BookListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        book_mapping = {book.id: book for book in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for book_id, data in data_mapping.items():
            book = book_mapping.get(book_id, None)
            if book is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(book, data))

        # Perform deletions.
        for book_id, book in book_mapping.items():
            if book_id not in data_mapping:
                book.delete()

        return ret


class BookSerializer1(serializers.Serializer):
    # We need to identify elements in the list using their primary key,
    # so use a writable field here, rather than the default which would be read-only.
    id = serializers.IntegerField()
    ...

    class Meta:
        models = Book
        fields = '__all__'
        list_serializer_class = BookListSerializer

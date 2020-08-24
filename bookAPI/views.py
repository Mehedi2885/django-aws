from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import FilterSet
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
from django.http import QueryDict
from django.http import HttpRequest, HttpResponse
import re

from bookAPI.serializers import BookSerializer, FooSerializer, BookSerializer1
from bookAPI.models import Book
from bookAPI.permission import UpdateOwnBookProfile


class BookFilter(FilterSet):
    name = filters.CharFilter(method='search_by_name')
    author = filters.CharFilter(method='search_by_author')

    class Meta:
        model = Book
        fields = ('name', 'author')

    def search_by_author(self, queryset, name, value):
        queryset = queryset.filter(author__icontains=value)
        return queryset

    def search_by_name(self, queryset, name, value):
        queryset = queryset.filter(name__icontains=value)
        return queryset


class BookApiModelViewSet(ModelViewSet):
    """Handle creating and updating book profile"""
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    http_method_names = ('get', 'post', 'put', 'patch')
    filter_backends = (DjangoFilterBackend,)
    filter_class = BookFilter


# class BookApiViewSet(ModelViewSet):
#     """Handle creating and updating book profile"""
#     serializer_class = BookSerializer
#     queryset = Book.objects.all()
#     http_method_names = ('get', 'post', 'put', 'patch')
#     """DjangoFilterBackend return by name or author ?name=<>, Ordering with
#     specific order like name or author alphabetically, SearchFilter with ?search=<anything>"""
#     filter_backends = (DjangoFilterBackend,)  # OrderingFilter, SearchFilter)
#     # filter_fields = {'name': ['icontains'], 'author': ['icontains']}
#     filter_class = BookFilter
#     # ordering_fields = ('name', 'author')
#     # ordering = ('name',)  # Always return name in alphabetic order
#     # search_fields = ('name', 'author', 'id')


class BookApiViewList(generics.ListAPIView):
    """Handle creating and updating book profile"""
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        name = self.request.query_params.get('name', None)
        author = self.request.query_params.get('author', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        elif author is not None:
            queryset = queryset.filter(author__icontains=author)
        return queryset


class BookApiViewSet(ViewSet):
    """Creating api with viewset, mainly focusing on create method"""
    serializer_class = BookSerializer

    def get_object(self, pk):
        queryset = Book.objects.all()
        data = get_object_or_404(queryset, pk=pk)
        return data

    def list(self, request):
        queryset = Book.objects.all()
        serializer_data = self.serializer_class(queryset, many=True)
        return Response(serializer_data.data)

    def retrieve(self, request, pk=None):
        data = self.get_object(pk)
        serializer_data = self.serializer_class(data)
        return Response(serializer_data.data)

    def create(self, request):
        serializers_data = self.serializer_class(data=request.data)
        if serializers_data.is_valid():
            serializers_data.save()
            return Response(serializers_data.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):

        book_data = self.get_object(pk)
        serializers_data = self.serializer_class(book_data, data=request.data, partial=True)
        if serializers_data.is_valid():
            serializers_data.save()
            return Response(serializers_data.validated_data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializers_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        book_data = self.get_object(pk)
        book_data.delete()
        return Response({'message': 'Source deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class BookBulkUpdateView(generics.ListAPIView, generics.UpdateAPIView):
    serializer_class = BookSerializer

    # def get_queryset(self):
    #     queryset = Book.objects.all()
    #     name = self.request.query_params.get('name', None)
    #     author = self.request.query_params.get('author', None)
    #     if name is not None:
    #         queryset = queryset.filter(name__icontains=name)
    #     elif author is not None:
    #         queryset = queryset.filter(author__icontains=author)
    #     return queryset

    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    # serializer_class.data

    def get_queryset(self):
        queryset = Book.objects.all()
        name = self.request.query_params.get('name', None)
        author = self.request.query_params.get('author', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        elif author is not None:
            queryset = queryset.filter(author__icontains=author)
        return queryset

    def put(self, request, *args, **kwargs):
        # queryset = Book.objects.all()
        # data = get_object_or_404(queryset)
        # # queryset = Book.objects.all()
        data = request.data
        print(data)
        serializer_data = self.serializer_class(data=data, many=True)
        print(serializer_data.validated_data)
        # serializer_data.data

        if serializer_data.is_valid():
            serializer_data.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FooView(generics.ListAPIView, generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer1

    def get_queryset(self):
        queryset = Book.objects.all()
        name = self.request.query_params.get('name', None)
        author = self.request.query_params.get('author', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        elif author is not None:
            queryset = queryset.filter(author__icontains=author)
        return queryset

    # def put(self, request, *args, **kwargs):
    #     # queryset = Book.objects.all()
    #     # data = get_object_or_404(queryset)
    #     # # queryset = Book.objects.all()
    #     data = request.data
    #     serializer_data = self.serializer_class(data=data, many=True)
    #     # serializer_data.data
    #
    #     if serializer_data.is_valid():
    #         serializer_data.save()
    #         return Response(status=status.HTTP_200_OK)
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)


__all__ = [
    # 'BulkCreateModelMixin',
    # 'BulkDestroyModelMixin',
    'BulkUpdateModelMixin'
]


class BulkUpdateModelMixin(object):
    """
    Update model instances in bulk by using the Serializers
    ``many=True`` ability from Django REST >= 2.2.5.
    """
    queryset = Book.objects.all()
    serializer_class = FooSerializer

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        if lookup_url_kwarg in self.kwargs:
            return super(BulkUpdateModelMixin, self).get_object()

        # If the lookup_url_kwarg is not present
        # get_object() is most likely called as part of options()
        # which by default simply checks for object permissions
        # and raises permission denied if necessary.
        # Here we don't need to check for general permissions
        # and can simply return None since general permissions
        # are checked in initial() which always gets executed
        # before any of the API actions (e.g. create, update, etc)
        return

    def bulk_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        # restrict the update to the filtered queryset
        serializer = self.get_serializer(
            self.filter_queryset(self.get_queryset()),
            data=request.data,
            many=True,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_bulk_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.bulk_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()

    def perform_bulk_update(self, serializer):
        return self.perform_update(serializer)


class BookBulkUpdateTry(ViewSet):
    serializer_class = BookSerializer

    def get_object(self, pk):
        queryset = Book.objects.all()
        data = get_object_or_404(queryset, pk=pk)
        return data

    def list(self, request):
        queryset = Book.objects.all()
        serializer_data = self.serializer_class(queryset, many=True)
        return Response(serializer_data.data)

    def retrieve(self, request, pk=None):
        data = self.get_object(pk)
        serializer_data = self.serializer_class(data)
        return Response(serializer_data.data)

    def put(self, request, pk=None):
        for id in pk:
            book_id = Book.objects.filter(id=id)
            book_data = self.get_object(book_id)
            serializers_data = self.serializer_class(book_data, instance=request.data, partial=True)
            if serializers_data.is_valid():
                serializers_data.save()
                return Response({'message': 'source updated successfully'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializers_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BookTry(APIView):

    def get_object(self, obj_id):
        try:
            return Book.objects.get(id=obj_id)
        except (Book.DoesNotExist, ValidationError):
            raise status.HTTP_400_BAD_REQUEST

    def validate_ids(self, id_list):
        for id in id_list:
            try:
                Book.objects.get(id=id)
            except (Book.DoesNotExist, ValidationError):
                raise status.HTTP_400_BAD_REQUEST
        return True

    def put(self, request, *args, **kwargs):

        data = request.data
        book_ids = [i['id'] for i in data]
        print("book_ids = ", book_ids)
        print(type(book_ids))
        self.validate_ids(book_ids)
        instances = []
        for temp_dict in data:
            book_id = temp_dict['id']
            name = temp_dict['name']
            author = temp_dict['author']
            obj = self.get_object(book_id)
            obj.name = name
            obj.description = author
            obj.save()
            instances.append(obj)
        serializer = BookSerializer(instances, many=True)
        return Response(serializer.data)


class BookDemo(APIView):
    def get_object(self, obj_id):
        try:
            return Book.objects.get(id=obj_id)
        except (Book.DoesNotExist, ValidationError):
            raise status.HTTP_400_BAD_REQUEST
    def validate_ids(self, id_list):
        for id in id_list:
            try:
                Book.objects.get(id=id)
            except (Book.DoesNotExist, ValidationError):
                raise status.HTTP_400_BAD_REQUEST
        return True
    def put(self, request, *args, **kwargs):
        request_data = request.data
        a = self.kwargs.get('id')
        print('value of a = ', a)
        y = request.get_full_path()
        print(y)
        x = re.search("(?<=3D)[^\]]+(\d)", y).group()
        print("x = ", x)
        print("type of x = ", type(x))
        z = (x.split(","))
        print("z = ", z)
        print(type(z))
        for i in range(0, len(z)):
            z[i] = int(z[i])
        print("After modification: ", z)
        self.validate_ids(z)
        instances = []
        for a, b in zip(z, request_data):
            name = b['name']
            author = b['author']
            obj = self.get_object(a)
            obj.name = name
            obj.author = author
            obj.save()
            instances.append(obj)
        serializer = BookSerializer(instances, many=True)
        return Response(serializer.data)

        # for temp_dict in request_data :
        #     # book_id = [z[i] for i in z]
        #     for i in z:
        #         name = temp_dict['name']
        #         author = temp_dict['author']
        #         # obj = self.get_object(i)
        #         # for i in z:
        #             # name = temp_dict['name']
        #             # author = temp_dict['author']
        #         obj = self.get_object(i)
        #         obj.name = name
        #         obj.author = author
        #         obj.save()
        #         instances.append(obj)
            # try:
            #     obj = self.get_object(z[i] for i in z)
            # except IndexError:
            #     pass
            # obj.name = name

            # obj.description = author
            # obj.save()
            # instances.append(obj)



        # instance = []
        # for i in z:
        #     obj = Book.objects.filter(id=i)
        #     obj.save()
        #     instance.append(obj)
        #
        # serializer_data = self.book_serializer(instance, many=True)
        # if serializer_data.is_valid():
        #     serializer_data.save()
        #     # .request .body
        #     # save.db()
        #
        # # print (x.startWith('%3D'))
        # # x= (request.get_full_path()[-2])
        # print(request.data)
        # return Response(serializer_data.data)






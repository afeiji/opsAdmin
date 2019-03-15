#encoding:utf-8
from rest_framework import viewsets, permissions, filters
from .models import Publish, Book,Author
from .serilalizers import PublishSerializer, BookSerializer, AuthorSerializer
from .filters import PublishFilter, BookFilter

class PublishViewSet(viewsets.ModelViewSet):
    # authentication_classes = (permissions.JS)
    permission_classes =  (permissions.IsAuthenticated, )
    queryset = Publish.objects.all()
    serializer_class = PublishSerializer

    filter_class = PublishFilter
    filter_fields = ("name","city")


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_class = BookFilter
    filter_fields = ("name","authors__name","publisher__name")

    ordering_fields = ('publication_date')

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
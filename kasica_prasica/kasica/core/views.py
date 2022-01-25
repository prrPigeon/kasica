from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Currency, Category, Transaction
from .serializers import CurrencySerializer, CategorySerializer, ReadTransactionSerializer, WriteTransactionSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    # if you don't wont to show pa0gination
    # pagination_class = None


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionModelViewSet(ModelViewSet):
    # queryset = Transaction.objects.all()

    # next queryset will speed up query, a lot !!!
    queryset = Transaction.objects.select_related("currency", "category")

    serializer_class = ReadTransactionSerializer

    # filter with query wit SearchFilter over description, and OrderingFilter by desending ordering_fields
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("description", )
    ordering_fields = ("amount", "date")

    filterset_fields = ("currency__code",)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer
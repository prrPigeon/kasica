from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Currency, Category, Transaction
from .serializers import CurrencySerializer, CategorySerializer, ReadTransactionSerializer, WriteTransactionSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    # if you don't wont to show pa0gination
    # pagination_class = None


class CategoryModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    # queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        """ return related categories"""
        return Category.objects.filter(user=self.request.user)


class TransactionModelViewSet(ModelViewSet):
    # authentication is required with Api Key (Token <value>) in Authorization header
    permission_classes = (IsAuthenticated,)

    # queryset = Transaction.objects.all()

    serializer_class = ReadTransactionSerializer

    # filter with query wit SearchFilter over description, and OrderingFilter by desending ordering_fields
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("description", )
    ordering_fields = ("amount", "date")

    filterset_fields = ("currency__code",)

    def get_queryset(self):
        # next queryset will speed up query, a lot !!!
        return Transaction.objects.select_related("currency", "category", "user").filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer

    # def perform_create(self, serializer):
    #     """
    #     will allow only auth user to write to itself.
    #     """
    #     serializer.save(user=self.request.user)
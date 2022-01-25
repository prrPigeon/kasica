from rest_framework import serializers
from .models import Currency, Category, Transaction


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class WriteTransactionSerializer(serializers.ModelSerializer):
    # will allow to show code (which is unique) instead of id
    currency = serializers.SlugRelatedField(slug_field="code", queryset=Currency.objects.all())

    class Meta:
        model = Transaction
        fields = (
            # "id",
            "amount",
            "currency",
            "date",
            "description",
            "category",
        )


class ReadTransactionSerializer(serializers.ModelSerializer):
    # will allow to show currency key as a object
    currency = CurrencySerializer()
    category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "amount",
            "currency",
            "date",
            "description",
            "category",
        )
        read_only_fields = fields

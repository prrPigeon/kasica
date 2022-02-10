from rest_framework import serializers
from rest_framework.authtoken.admin import User

from core.reports import ReportParams

from .models import Currency, Category, Transaction


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name")


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ("id", "user", "name")


class WriteTransactionSerializer(serializers.ModelSerializer):

    # after declare this instance, it's safe to remove perform_create method from viewss
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) #>> new user

    # will allow to show code (which is unique) instead of id
    currency = serializers.SlugRelatedField(slug_field="code", queryset=Currency.objects.all())

    class Meta:
        model = Transaction
        fields = (
            # "id",
            # "user", # but this conf will allow user to create on another user, just with token auth. >>> old user
            "user",
            "amount",
            "currency",
            "date",
            "description",
            "category",
        )

    def __init__(self, *args, **kwargs):
        """
        rewrite init to disable feature of user using others categories,
        but retrieve only categories related to context user!!!
        """
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        # self.fields["category"].queryset = Category.objects.filter(user=user) # or
        self.fields["category"].queryset = user.categories.all()


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")
        read_only_fields = fields


class ReadTransactionSerializer(serializers.ModelSerializer):
    # will allow to show currency key as a object
    currency = CurrencySerializer()
    category = CategorySerializer()

    user = ReadUserSerializer()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "amount",
            "currency",
            "date",
            "description",
            "category",
            "user", # but this conf will allow user to see transaction off another user, just with token auth. And must add user on queryset in TransactionModelViewSet.
        )
        read_only_fields = fields


class ReportEntrySerializer(serializers.Serializer):
    category = CategorySerializer()
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=15, decimal_places=2)



class ReportParamsSerializer(serializers.Serializer):
    """To achive returning personal reports to authenticated user,
    cause previous return all bulk reports!!!"""
    
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    # current user
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        return ReportParams(**validated_data)
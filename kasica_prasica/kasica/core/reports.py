import datetime
from dataclasses import dataclass
from decimal import Decimal

from django.db.models import Sum, Count, Avg
from django.contrib.auth.models import User

from core.models import Transaction, Category


@dataclass
class ReportEntry:
    """will return a category as object"""
    category: Category
    total: Decimal
    count: int
    avg: Decimal

@dataclass
class ReportParams:
    start_date : datetime.datetime
    end_date : datetime.datetime
    user : User

def transaction_report(params: ReportParams):
    data = []
    """
    return report as list of objects if format
    [
    {
        'category': n,
        'total': n,
        'count': n,
        'avg': n,
    },
    ...
    ]
    """
    queryset = Transaction.objects.filter(
        user=params.user,
        date__gte=params.start_date,
        date__lte=params.end_date
    ).values("category").annotate(
        total=Sum("amount"),
        count=Count("id"),
        avg=Avg("amount")
    )

    categories_index = {}
    """ to avoid multiple queries, there is 6 while creating one report,
        some kind of cashing is implemented with categories index dict
    """
    for category in Category.objects.filter(user=params.user):
        categories_index[category.pk] = category

    for entry in queryset:
        # category = Category.objects.get(pk=entry["category"])
        category = categories_index.get(entry["category"])

        report_entry = ReportEntry(
            category, entry["total"], entry["count"], entry["avg"]
        )
        data.append(report_entry)
    return data
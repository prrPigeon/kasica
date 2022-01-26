from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from core import views

# incosistent usage of "" and '' can be fixed with Black module (check that)

router = routers.SimpleRouter()
router.register(r'categories', views.CategoryModelViewSet, basename="category")
router.register(r'transactions', views.TransactionModelViewSet, basename="transaction")


urlpatterns = [
    path('admin/', admin.site.urls),
    # to obtain auth token
    path('login/', obtain_auth_token, name="obtain_auth_token"),
    path('currencies/', views.CurrencyListAPIView.as_view(), name="currencies")
] + router.urls

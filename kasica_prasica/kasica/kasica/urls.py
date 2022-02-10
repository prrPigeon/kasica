import debug_toolbar

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from core import views

# incosistent usage of "" and '' can be fixed with Black module (check that)

router = routers.SimpleRouter()
router.register(r'categories', views.CategoryModelViewSet, basename="category")
router.register(r'transactions', views.TransactionModelViewSet, basename="transaction")


urlpatterns = [
    path('admin/', admin.site.urls),
    # path for session based auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # to obtain auth token
    path('login/', obtain_auth_token, name="obtain_auth_token"),
    path('currencies/', views.CurrencyListAPIView.as_view(), name="currencies"),
    path('report/', views.TransactionReportAPIView.as_view(), name="report" ),
    # path for debug toolbar
    path('__debug__/', include(debug_toolbar.urls))
] + router.urls

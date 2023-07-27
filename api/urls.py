from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import path

from .views import (
    DishListApi,
    DishCreateApi,
    OrderCreateApi,
    OrderListApi,
    OrderActiveListApi,
    OrderStatusUpdateApi
)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("dishes/", DishListApi.as_view()),
    path("create-dish/", DishCreateApi.as_view()),
    path("create-order/", OrderCreateApi.as_view()),
    path("orders/", OrderListApi.as_view()),
    path("active-orders/", OrderActiveListApi.as_view()),
    path("orders/<str:pk>/status/", OrderStatusUpdateApi.as_view(), name='order_status'),
]

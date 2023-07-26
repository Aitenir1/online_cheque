# Thrid-party
from rest_framework import generics

# Django
from django.db.models.functions import TruncDate

# Local Django
from .models import Dish, Order
from .serializers import DishSerializer, OrderSerializer, OrderGetSerializer
from .utils.pagination import OrderGetApiPagination


class DishListApi(generics.ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class OrderCreateApi(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderListApi(generics.ListAPIView):
    serializer_class = OrderGetSerializer
    pagination_class = OrderGetApiPagination

    def get_queryset(self):
        date = self.request.query_params.get('date')
        if date is not None:
            print(date)
            orders = Order.objects.annotate(
                date=TruncDate('time_created')
            ).filter(date=date)

            return orders
        return Order.objects.all()

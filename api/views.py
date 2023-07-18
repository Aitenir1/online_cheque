# Thrid-party
from rest_framework import generics

# Django
from django.db.models.functions import TruncDate

# Local Django
from .models import Dish, Order
from .serializers import DishSerializer, OrderSerializer


class DishListApi(generics.ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class OrderCreateApi(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderListApi(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date')

        orders = Order.objects.annotate(
            date=TruncDate('time_created')
        ).filter(date=date)

        return orders

# Thrid-party

# Django
from django.db.models.functions import TruncDate
from rest_framework.response import Response
from rest_framework import generics, status

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


class OrderStatusUpdateApi(generics.UpdateAPIView):
    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        order.status = 1
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status.HTTP_200_OK)

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


class OrderActiveListApi(generics.ListAPIView):
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        return Order.objects.filter(status=0)

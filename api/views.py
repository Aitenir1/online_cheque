# Thrid-party
import sh

# Django
from django.utils import timezone
from django.db.models.functions import TruncDate
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView



# Local Django
from .models import Dish, Order, Category
from .serializers import DishSerializer, DishCreateSerializer, OrderSerializer, OrderGetSerializer, CategorySerializer



# Utils
from .utils.pagination import OrderGetApiPagination
from .utils.print_receipt import print_receipt

class CategoryListApi(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DishListApi(generics.ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DishCreateApi(generics.CreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishCreateSerializer


class OrderCreateApi(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderStatusUpdateApi(generics.UpdateAPIView):

    def patch(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        order.status = 1
        order.save()

        print_receipt(order)

        serializer = OrderGetSerializer(order)

        return Response(serializer.data, status.HTTP_200_OK)


class OrderListApi(generics.ListAPIView):
    serializer_class = OrderGetSerializer
    pagination_class = OrderGetApiPagination

    def get_queryset(self):

        date = self.request.query_params.get('date')
        if date is not None:
            orders = Order.objects.annotate(
                date=TruncDate('time_created')
            ).filter(date=date)

            return orders
        return Order.objects.all()


class OrderActiveListApi(generics.ListAPIView):
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        return Order.objects.filter(status=0)


class ReceiptPrintApi(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')

        if order_id is None:
            return Response({"Message": "order_id can not be None"})
        print(order_id)
        order_to_print = Order.objects.get(pk=order_id)

        print_receipt(order_to_print)

        return Response({"Message": "Receipt was printer successfully"})


class OrderWeekListApi(generics.ListAPIView):
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=7)

        print(f"START: {start_date}")
        print(f"END:   {end_date}")

        return Order.objects.filter(time_created__range=[start_date, end_date])


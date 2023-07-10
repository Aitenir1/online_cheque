# Thrid-party
from rest_framework import viewsets, generics, views

# Django
from django.shortcuts import render, redirect, HttpResponse

# Local Django
from .models import Dish, Order
from .serializers import DishSerializer, OrderSerializer, OrderGetSerializer


class DishListApi(generics.ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class OrderCreateApi(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
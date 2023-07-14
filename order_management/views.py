from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from api.models import Order

class OrdersLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy('home')


class OrdersListView(ListView, LoginRequiredMixin):
    model = Order
    template_name = 'home.html'

    context_object_name = 'orders'


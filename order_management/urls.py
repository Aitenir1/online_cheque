from django.urls import path, include

from .views import OrdersLoginView, OrdersListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', OrdersLoginView.as_view(), name="login"),
    path('home/', login_required(OrdersListView.as_view()), name="home")
]
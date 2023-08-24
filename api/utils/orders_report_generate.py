from typing import Union, List
from django.db.models import QuerySet
from api.models import Order

def orders_report_generate(orders: Union[QuerySet, List[Order]]):
    for order in orders:
        pass
    pass

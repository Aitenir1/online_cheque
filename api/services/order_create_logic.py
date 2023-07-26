from collections import OrderedDict

from rest_framework import serializers

from ..models import Table, Order, OrderItem

def create_order_from_json(
        table: Table,
        order_items: list[OrderedDict],
        payment: int,
        is_takeaway: int,
        comment: str

):
    order = Order.objects.get_or_create(table=table, status=0)[0]

    try:
        order.table = table
        order.payment = payment
        order.is_takeaway = is_takeaway
        order.comment = comment

        total_price = order.total_price

        for order_item in order_items:
            dish = order_item['dish']
            quantity = order_item['quantity']
            additives = order_item['additives']

            for additive in additives:
                total_price += additive.price

                if additive.dish != dish:
                    raise serializers.ValidationError(f'{dish.name_en} does not have {additive.name_en} additive')

            order_item_obj, created = OrderItem.objects.get_or_create(dish=dish, order=order)

            if created:
                order_item_obj.quantity = quantity
            else:
                order_item_obj.quantity += quantity

            for additive in additives:
                order_item_obj.additives.add(additive)

            order_item_obj.save()

            total_price += dish.price * quantity
        order.total_price = total_price

        order.save()

        return order

    except serializers.ValidationError:
        print("Error has occured during creating a new Order")
        order.delete()
        raise


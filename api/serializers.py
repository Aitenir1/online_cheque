
from rest_framework import serializers
from .models import Dish, Category, Table, Order, OrderItem, Additive


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'url']


class AdditiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additive
        fields = '__all__'


class DishSerializer(serializers.HyperlinkedModelSerializer):
    category_name = serializers.SerializerMethodField()
    additives = AdditiveSerializer(many=True)

    class Meta:
        model = Dish
        fields = ['id', 'name_en', 'name_kg', 'name_ru',
                  'description_en', 'description_kg', 'description_ru',
                  'price', 'gram', 'category_name', 'image', 'additives',
                  'is_trend']

    @staticmethod
    def get_category_name(obj):
        return obj.category.name


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity', 'additives']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    time_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Order
        fields = ['id', 'table', 'time_created', 'status', 'comment', 'payment', 'is_takeaway', 'total_price', 'items']

    def create(self, validated_data: dict):
        try:
            order_items = validated_data.pop('items')
            table = validated_data.pop('table')
            print(order_items)
            order = Order.objects.get_or_create(table=table, status=0)[0]
            total_sum = order.total_price
            for order_item in order_items:

                dish = order_item['dish']
                quantity = order_item['quantity']
                additives = order_item['additives']

                for additive in additives:
                    total_sum += additive.price

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

                print("===================")
                print(f'{dish.price=}')
                print(f'{order_item_obj.quantity}')
                total_sum += dish.price * quantity

            order.total_price = total_sum

        except serializers.ValidationError:
            order.delete()
            raise

        comment = validated_data.get('comment', '-')
        payment = validated_data.get('payment', 0)
        is_takeaway = validated_data.get('is_takeaway', 0)

        order.comment = comment
        order.payment = payment
        order.is_takeaway = is_takeaway

        order.save()

        return order


class OrderItemGetSerializer(serializers.ModelSerializer):
    dish = DishSerializer()
    additives = AdditiveSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderGetSerializer(serializers.ModelSerializer):
    items = OrderItemGetSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

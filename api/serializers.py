
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
                  'is_trend',]

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
            order = Order.objects.create(**validated_data)

            total_sum = 0
            for order_item in order_items:

                dish = order_item['dish']
                quantity = order_item['quantity']
                additives = order_item['additives']

                for additive in additives:
                    total_sum += additive.price
                    if additive.dish != dish:
                        raise serializers.ValidationError(f'{dish.name_en} does not have {additive.name_en} additive')

                order_item_obj = OrderItem.objects.create(
                    dish=dish,
                    order=order,
                    quantity=quantity
                )

                for additive in additives:
                    order_item_obj.additives.add(additive)

                order_item_obj.save()

                total_sum += dish.price * quantity

            order.total_price = total_sum

        except serializers.ValidationError:
            order.delete()
            raise

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

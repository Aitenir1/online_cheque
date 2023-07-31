from uuid import UUID
from asgiref.sync import async_to_sync
import json

from rest_framework import serializers
from channels.layers import get_channel_layer

from .models import Dish, Category, Table, Order, OrderItem, Additive, OrderComment
from .json_encoders import UUIDEncoder
from .utils.order_create_logic import create_order_from_json


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class TableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'url']


class AdditiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additive
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderComment
        # fields = ['id', 'body']
        fields = ['body']

class DishSerializer(serializers.HyperlinkedModelSerializer):
    category_name = serializers.SerializerMethodField()
    # category = CategorySerializer()
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


class DishCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Dish
        fields = '__all__'

    def create(self, validated_data):
        category, created = Category.objects.get_or_create(name=validated_data.pop('category').get('name'))
        dish = Dish.objects.create(**validated_data)
        dish.category = category

        return dish

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity', 'additives']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    # comments = CommentSerializer(many=True, required=False)
    # comment = serializers.SerializerMethodField('_get_comment')
    comment = serializers.CharField()
    time_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Order
        fields = ['id', 'table', 'time_created', 'status', 'payment', 'is_takeaway', 'total_price', 'items', 'comment']

    def create(self, validated_data: dict):
        print(validated_data)
        table = validated_data.pop('table')
        order_items = validated_data.pop('items')
        payment = validated_data.get('payment', 0)
        is_takeaway = validated_data.get('is_takeaway', 0)
        comment = validated_data.get('comment', '-')

        order = create_order_from_json(
            table=table,
            order_items=order_items,
            payment=payment,
            is_takeaway=is_takeaway,
            comment=comment
        )
        # print(comment)
        self.notify_consumer(instance=order)

        return order

    def notify_consumer(self, instance) -> None:
        channel_layer = get_channel_layer()

        serializer = OrderSerializer(instance)
        order_json = json.dumps(serializer.data, cls=UUIDEncoder)

        async_to_sync(channel_layer.group_send)(
            'model_instances',
            {
                'type': 'send_model_instance',
                'instance': order_json
            }
        )

class OrderItemGetSerializer(serializers.ModelSerializer):
    dish = DishSerializer()
    additives = AdditiveSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity', 'additives']


class OrderGetSerializer(serializers.ModelSerializer):
    items = OrderItemGetSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'table', 'time_created', 'status', 'comments', 'payment', 'is_takeaway', 'total_price', 'items']

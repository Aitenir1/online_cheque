from asgiref.sync import async_to_sync
import json


from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer

from .models import Order
from .serializers import OrderSerializer


@receiver(post_save, sender=Order)
def notify_clients(sender, instance: Order, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()

        order_json = json.dumps(OrderSerializer(instance).data)

        async_to_sync(channel_layer.group_send)(
            'model_instances',
            {
                'type': 'send_model_instance',
                'instance': order_json
            }
        )
import uuid

from django.db import models

class Table(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "table"

    def __str__(self):
        return f"{self.id}"

class Dish(models.Model):
    TREND_CHOINCES = (
        (0, 'Trend'),
        (1, 'Not trend')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name_en = models.CharField(max_length=200)
    name_kg = models.CharField(max_length=200, default='Тамак')
    name_ru = models.CharField(max_length=200, default='Еда')
    description_en = models.TextField()
    description_kg = models.TextField(default='Тамак')
    description_ru = models.TextField(default='Еда')
    price = models.FloatField()
    gram = models.CharField(max_length=100, default='200')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(default='food1.png', upload_to='dishes/')
    is_trend = models.IntegerField(choices=TREND_CHOINCES, default=0)

    class Meta:
        db_table = "dish"

    def __str__(self):
        return f"{self.name_en} | {self.price}"


class Additive(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name_en = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)
    name_kg = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='additives')

    class Meta:
        db_table = "additive"

    def __str__(self):
        return f"{self.dish.name_en} + {self.name_en}"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "category"

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):

    STATUS_CHOICES = (
        (0, 'In progress'),
        (1, 'Completed'),
    )

    TAKEAWAY_CHOICES = (
        (0, 'Here'),
        (1, 'Takeaway order'),
    )

    PAYMENT_CHOICES = (
        (0, 'Cash'),
        (1, 'Terminal')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    table = models.ForeignKey('Table', on_delete=models.DO_NOTHING)
    time_created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    comment = models.TextField(default="-")
    is_takeaway = models.IntegerField(choices=TAKEAWAY_CHOICES, default=0)
    payment = models.IntegerField(choices=PAYMENT_CHOICES, default=0)
    total_price = models.PositiveIntegerField(default=0, blank=True, null=True, editable=False)

    def __str__(self):
        return f"This order | {self.total_price}"

    class Meta:
        db_table = "order"
        ordering = ['status', 'time_created']

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    additives = models.ManyToManyField(Additive, blank=True)

    class Meta:
        db_table = "order_item"

# Generated by Django 4.2.2 on 2023-07-08 16:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Additive',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name_en', models.CharField(max_length=50)),
                ('name_ru', models.CharField(max_length=50)),
                ('name_kg', models.CharField(max_length=50)),
                ('price', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'additive',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name_en', models.CharField(max_length=200)),
                ('name_kg', models.CharField(default='Тамак', max_length=200)),
                ('name_ru', models.CharField(default='Еда', max_length=200)),
                ('description_en', models.TextField()),
                ('description_kg', models.TextField(default='Тамак')),
                ('description_ru', models.TextField(default='Еда')),
                ('price', models.FloatField()),
                ('gram', models.CharField(default='200', max_length=100)),
                ('image', models.ImageField(default='food1.png', upload_to='dishes/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
            ],
            options={
                'db_table': 'dish',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'In progress'), (1, 'Completed')], default=0)),
                ('is_takeaway', models.IntegerField(choices=[(0, 'Here'), (1, 'Takeaway order')], default=0)),
                ('payment', models.IntegerField(choices=[(0, 'Cash'), (1, 'Terminal')], default=0)),
                ('total_price', models.PositiveIntegerField(blank=True, default=0, editable=False, null=True)),
            ],
            options={
                'db_table': 'order',
                'ordering': ['status', 'time_created'],
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'table',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('additives', models.ManyToManyField(blank=True, to='api.additive')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.dish')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.order')),
            ],
            options={
                'db_table': 'order_item',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.table'),
        ),
        migrations.AddField(
            model_name='additive',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additives', to='api.dish'),
        ),
    ]
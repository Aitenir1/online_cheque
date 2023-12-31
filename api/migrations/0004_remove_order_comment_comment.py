# Generated by Django 4.2.2 on 2023-07-31 15:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_dish_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='comment',
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('body', models.TextField(default='-')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
            options={
                'db_table': 'comment',
            },
        ),
    ]

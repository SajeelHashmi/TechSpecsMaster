# Generated by Django 5.0.2 on 2024-02-24 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_mobilephone'),
    ]

    operations = [
        migrations.CreateModel(
            name='TV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenSize', models.CharField(max_length=255)),
                ('screenType', models.CharField(max_length=255)),
                ('resolution', models.CharField(max_length=255)),
                ('threeD', models.CharField(max_length=255)),
                ('HD', models.CharField(max_length=255)),
                ('fourK', models.CharField(max_length=255)),
                ('SmartTv', models.CharField(max_length=255)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]

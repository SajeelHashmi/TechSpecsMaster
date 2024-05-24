# Generated by Django 5.0.2 on 2024-02-24 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_tablet'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmartWatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strapMaterial', models.CharField(max_length=255)),
                ('waterResistance', models.CharField(max_length=255)),
                ('os', models.CharField(max_length=255)),
                ('speaker', models.CharField(max_length=255)),
                ('mode', models.CharField(max_length=255)),
                ('screenSize', models.CharField(max_length=255)),
                ('resolution', models.CharField(max_length=255)),
                ('screenType', models.CharField(max_length=255)),
                ('ram', models.CharField(max_length=255)),
                ('rom', models.CharField(max_length=255)),
                ('wifi', models.CharField(max_length=255)),
                ('batteryCapacity', models.CharField(max_length=255)),
                ('batteryLife', models.CharField(max_length=255)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]

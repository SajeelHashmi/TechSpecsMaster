# Generated by Django 5.0.2 on 2024-02-24 12:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_wirelessearbuds'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tablet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realeseDate', models.CharField(max_length=255)),
                ('simSupport', models.CharField(max_length=255)),
                ('dimensions', models.CharField(max_length=255)),
                ('weight', models.CharField(max_length=255)),
                ('os', models.CharField(max_length=255)),
                ('screenSize', models.CharField(max_length=255)),
                ('resolution', models.CharField(max_length=255)),
                ('screenType', models.CharField(max_length=255)),
                ('internalMemory', models.CharField(max_length=255)),
                ('ram', models.CharField(max_length=255)),
                ('cardSlot', models.CharField(max_length=255)),
                ('processor', models.CharField(max_length=255)),
                ('gpu', models.CharField(max_length=255)),
                ('battery', models.CharField(max_length=255)),
                ('frontCamera', models.CharField(max_length=255)),
                ('backCamera', models.CharField(max_length=255)),
                ('bluetooth', models.CharField(max_length=255)),
                ('wifi', models.CharField(max_length=255)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]

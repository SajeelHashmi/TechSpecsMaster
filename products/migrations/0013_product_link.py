# Generated by Django 5.0.2 on 2024-03-12 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_store_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='link',
            field=models.CharField(default='', max_length=2083),
        ),
    ]
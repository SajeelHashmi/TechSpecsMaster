# Generated by Django 5.0.3 on 2024-04-05 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_rename_review_review_buildreview_review_genralreview_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='genralReview',
            new_name='generalReview',
        ),
    ]

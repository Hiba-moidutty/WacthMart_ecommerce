# Generated by Django 4.1.3 on 2023-01-10 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Variation', '0001_initial'),
        ('cart', '0004_cartitem_variant_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='Variation.variation'),
        ),
    ]

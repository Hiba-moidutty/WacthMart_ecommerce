# Generated by Django 4.1.3 on 2023-01-05 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Coupon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='coupon_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
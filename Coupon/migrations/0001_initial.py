# Generated by Django 4.1.3 on 2023-01-02 06:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=200)),
                ('coupon_limit', models.IntegerField()),
                ('validity_upto', models.DateField()),
                ('is_used', models.BooleanField(blank=True, default=False, null=True)),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxLengthValidator(100)])),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]

# Generated by Django 4.1.3 on 2022-12-10 08:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='otp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]

# Generated by Django 4.1.3 on 2022-12-22 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_rename_country_order_ordernote_remove_order_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='method',
            new_name='payment_method',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]

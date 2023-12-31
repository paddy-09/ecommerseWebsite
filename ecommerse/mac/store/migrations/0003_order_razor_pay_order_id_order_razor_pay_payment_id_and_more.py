# Generated by Django 4.2.5 on 2023-10-07 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_product_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="razor_pay_order_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="razor_pay_payment_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="razor_pay_payment_signature",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

# Generated by Django 5.0.4 on 2024-04-12 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainrobot', '0016_rename_pro_name_products_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='v2panel',
            name='panel_id',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
# Generated by Django 5.0.4 on 2024-04-11 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainrobot', '0015_alter_products_categori_id_alter_products_pro_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='pro_name',
            new_name='product_name',
        ),
    ]

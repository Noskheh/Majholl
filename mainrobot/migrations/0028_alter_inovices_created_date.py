# Generated by Django 5.0.4 on 2024-05-22 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainrobot', '0027_alter_inovices_gift_code_alter_v2panel_capcity_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inovices',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
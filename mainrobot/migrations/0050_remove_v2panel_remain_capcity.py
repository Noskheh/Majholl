# Generated by Django 5.0.4 on 2024-07-11 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainrobot', '0049_v2panel_remain_capcity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='v2panel',
            name='remain_capcity',
        ),
    ]
# Generated by Django 5.0.4 on 2024-06-19 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainrobot', '0042_alter_channels_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='v2panel',
            name='inbounds_selected',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]

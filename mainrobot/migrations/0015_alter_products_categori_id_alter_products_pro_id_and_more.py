# Generated by Django 5.0.4 on 2024-04-11 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainrobot', '0014_alter_v2panel_capcity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='categori_id',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='pro_id',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='sort_id',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
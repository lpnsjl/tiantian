# Generated by Django 2.0.1 on 2018-01-24 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_cart', '0003_auto_20180123_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartinfo',
            name='cnumber',
            field=models.IntegerField(),
        ),
    ]

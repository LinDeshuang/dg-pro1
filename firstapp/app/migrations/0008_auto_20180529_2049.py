# Generated by Django 2.0.5 on 2018-05-29 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20180529_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='gemail',
            field=models.EmailField(max_length=254),
        ),
    ]

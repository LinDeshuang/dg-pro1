# Generated by Django 2.0.5 on 2018-05-29 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180529_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='gaccount',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
# Generated by Django 2.0.5 on 2018-05-29 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180529_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishment',
            name='ptype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Nav'),
        ),
    ]

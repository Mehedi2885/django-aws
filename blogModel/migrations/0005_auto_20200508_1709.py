# Generated by Django 3.0.5 on 2020-05-08 17:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogModel', '0004_auto_20200508_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='publish_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
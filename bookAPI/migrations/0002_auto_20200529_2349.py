# Generated by Django 2.2 on 2020-05-29 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]

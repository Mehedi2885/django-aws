# Generated by Django 2.2 on 2020-05-21 17:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('author', models.CharField(max_length=150)),
                ('published_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]

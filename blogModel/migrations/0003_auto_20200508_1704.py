# Generated by Django 3.0.5 on 2020-05-08 17:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogModel', '0002_auto_20200507_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='publish_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postmodel',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='title',
            field=models.CharField(max_length=150, unique=True, verbose_name='Post Title'),
        ),
    ]

# Generated by Django 3.0.5 on 2020-05-08 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogModel', '0006_postmodel_author_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]

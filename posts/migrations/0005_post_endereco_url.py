# Generated by Django 3.2.10 on 2022-02-09 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_remove_post_endereco_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='endereco_url',
            field=models.SlugField(null=True, unique=True),
        ),
    ]

# Generated by Django 3.2.10 on 2022-02-18 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_perfil_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='bio',
            field=models.CharField(default='Hello, World', max_length=100),
        ),
        migrations.AddField(
            model_name='perfil',
            name='foto',
            field=models.ImageField(default='default.png', upload_to=''),
        ),
    ]

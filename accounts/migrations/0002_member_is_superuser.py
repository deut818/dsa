# Generated by Django 3.1.2 on 2020-11-09 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
    ]

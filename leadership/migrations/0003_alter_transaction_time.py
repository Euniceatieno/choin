# Generated by Django 3.2.8 on 2021-10-28 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadership', '0002_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='time',
            field=models.DateField(auto_now_add=True),
        ),
    ]

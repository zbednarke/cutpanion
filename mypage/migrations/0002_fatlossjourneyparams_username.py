# Generated by Django 4.1.4 on 2023-01-12 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fatlossjourneyparams',
            name='username',
            field=models.CharField(default='', max_length=30),
        ),
    ]

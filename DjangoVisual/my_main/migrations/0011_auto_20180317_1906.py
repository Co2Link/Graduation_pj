# Generated by Django 2.0.2 on 2018-03-17 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_main', '0010_auto_20180311_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='fans_1_item_dj',
            name='description',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='fans_2_item_dj',
            name='description',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='fans_2_item_dj',
            name='screen_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]

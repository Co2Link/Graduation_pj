# Generated by Django 2.0.2 on 2018-03-07 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_main', '0002_auto_20180305_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapyItem',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('task_id', models.IntegerField()),
            ],
        ),
    ]
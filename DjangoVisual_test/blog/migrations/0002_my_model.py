# Generated by Django 2.0.2 on 2018-03-05 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='my_model',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('body', models.TextField()),
            ],
        ),
    ]

# Generated by Django 2.0.7 on 2019-04-07 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20190407_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
    ]

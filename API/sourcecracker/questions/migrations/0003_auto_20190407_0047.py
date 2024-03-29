# Generated by Django 2.0.7 on 2019-04-07 00:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sourcecracker.utils


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_sourceentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='created_by',
            field=models.ForeignKey(blank=True, default=sourcecracker.utils.current_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating_type',
            field=models.CharField(choices=[('is-long', 'Is long'), ('is-science', 'Is science'), ('is-complex', 'Is complex'), ('is-helpful', 'Is helpful')], max_length=32),
        ),
    ]

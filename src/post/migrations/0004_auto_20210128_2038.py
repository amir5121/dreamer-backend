# Generated by Django 3.1.4 on 2021-01-28 20:38

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20210128_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dream',
            name='voice',
            field=models.FileField(blank=True, null=True, upload_to=post.models.voice_upload_path),
        ),
    ]

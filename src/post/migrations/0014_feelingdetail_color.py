# Generated by Django 3.1.4 on 2020-12-18 08:43

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_post_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='feelingdetail',
            name='color',
            field=colorfield.fields.ColorField(default='#1F182E', max_length=18),
        ),
    ]

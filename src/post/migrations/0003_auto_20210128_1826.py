# Generated by Django 3.1.4 on 2021-01-28 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_dream_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dream',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]

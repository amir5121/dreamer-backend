# Generated by Django 3.1.3 on 2020-12-10 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20201210_0700'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feeling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField(default=0)),
                ('dream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feelings', to='post.dream')),
                ('feeling', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='post.feelingdetail')),
            ],
        ),
    ]

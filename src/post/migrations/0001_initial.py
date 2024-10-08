# Generated by Django 3.1.4 on 2021-01-14 10:10

import colorfield.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_better_admin_arrayfield.models.fields
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('publication_status', model_utils.fields.StatusField(choices=[('personal', 'personal'), ('published', 'published')], default='personal', max_length=100, no_check_for_status=True)),
                ('dream_clearance', models.PositiveSmallIntegerField(choices=[(0, 'Cloudy'), (1, 'Normal'), (2, 'Clear'), (3, 'Super clear')], default=1)),
                ('text', models.TextField()),
                ('title', models.TextField()),
                ('dream_date', models.DateTimeField()),
                ('voice', models.FileField(blank=True, null=True, upload_to='')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='FeelingDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_removed', models.BooleanField(default=False)),
                ('parent_type', models.CharField(choices=[('enjoyment', 'Enjoyment'), ('sadness', 'Sadness'), ('fear', 'Fear'), ('anger', 'Anger'), ('disgust', 'Disgust')], max_length=64)),
                ('detailed_type', models.CharField(blank=True, choices=[('enjoyment_happiness', 'enjoyment_happiness'), ('enjoyment_love', 'enjoyment_love'), ('enjoyment_relief', 'enjoyment_relief'), ('enjoyment_contentment', 'enjoyment_contentment'), ('enjoyment_amusement', 'enjoyment_amusement'), ('enjoyment_joy', 'enjoyment_joy'), ('enjoyment_pride', 'enjoyment_pride'), ('enjoyment_excitement', 'enjoyment_excitement'), ('enjoyment_peace', 'enjoyment_peace'), ('enjoyment_satisfaction', 'enjoyment_satisfaction'), ('enjoyment_compassion', 'enjoyment_compassion'), ('sadness_lonely', 'sadness_lonely'), ('sadness_heartbroken', 'sadness_heartbroken'), ('sadness_gloomy', 'sadness_gloomy'), ('sadness_disappointed', 'sadness_disappointed'), ('sadness_hopeless', 'sadness_hopeless'), ('sadness_grieved', 'sadness_grieved'), ('sadness_unhappy', 'sadness_unhappy'), ('sadness_lost', 'sadness_lost'), ('sadness_troubled', 'sadness_troubled'), ('sadness_resigned', 'sadness_resigned'), ('sadness_miserable', 'sadness_miserable'), ('fear_worried', 'fear_worried'), ('fear_doubtful', 'fear_doubtful'), ('fear_nervous', 'fear_nervous'), ('fear_anxious', 'fear_anxious'), ('fear_terrified', 'fear_terrified'), ('fear_panicked', 'fear_panicked'), ('fear_horrified', 'fear_horrified'), ('fear_desperate', 'fear_desperate'), ('fear_confused', 'fear_confused'), ('fear_stressed', 'fear_stressed'), ('anger_annoyed', 'anger_annoyed'), ('anger_frustrated', 'anger_frustrated'), ('anger_peeved', 'anger_peeved'), ('anger_contrary', 'anger_contrary'), ('anger_bitter', 'anger_bitter'), ('anger_infuriated', 'anger_infuriated'), ('anger_irritated', 'anger_irritated'), ('anger_mad', 'anger_mad'), ('anger_cheated', 'anger_cheated'), ('anger_vengeful', 'anger_vengeful'), ('anger_insulted', 'anger_insulted'), ('disgust_dislike', 'disgust_dislike'), ('disgust_revulsion', 'disgust_revulsion'), ('disgust_loathing', 'disgust_loathing'), ('disgust_disapproving', 'disgust_disapproving'), ('disgust_offended', 'disgust_offended'), ('disgust_horrified', 'disgust_horrified'), ('disgust_uncomfortable', 'disgust_uncomfortable'), ('disgust_nauseated', 'disgust_nauseated'), ('disgust_disturbed', 'disgust_disturbed'), ('disgust_withdrawal', 'disgust_withdrawal'), ('disgust_aversion', 'disgust_aversion')], max_length=64, null=True)),
                ('description', models.TextField()),
                ('color', colorfield.fields.ColorField(default='#1F182E', max_length=18)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('text', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('post_type', model_utils.fields.StatusField(choices=[('word_cloud', 'word_cloud'), ('timeline', 'timeline')], default='timeline', max_length=100, no_check_for_status=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Feeling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('dream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feelings', to='post.dream')),
                ('feeling', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='post.feelingdetail')),
            ],
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elements', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('type', models.CharField(choices=[('place', 'place'), ('character', 'character'), ('object', 'object')], max_length=64)),
                ('dream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='post.dream')),
            ],
        ),
    ]

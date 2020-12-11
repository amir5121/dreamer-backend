# Generated by Django 3.1.3 on 2020-12-10 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20201206_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeelingDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_removed', models.BooleanField(default=False)),
                ('parent_type', models.CharField(choices=[('enjoyment', 'Enjoyment'), ('sadness', 'Sadness'), ('fear', 'Fear'), ('anger', 'Anger'), ('disgust', 'Disgust')], max_length=64)),
                ('detailed_type', models.CharField(choices=[('enjoyment_happiness', 'enjoyment_happiness'), ('enjoyment_love', 'enjoyment_love'), ('enjoyment_relief', 'enjoyment_relief'), ('enjoyment_contentment', 'enjoyment_contentment'), ('enjoyment_amusement', 'enjoyment_amusement'), ('enjoyment_joy', 'enjoyment_joy'), ('enjoyment_pride', 'enjoyment_pride'), ('enjoyment_excitement', 'enjoyment_excitement'), ('enjoyment_peace', 'enjoyment_peace'), ('enjoyment_satisfaction', 'enjoyment_satisfaction'), ('enjoyment_compassion', 'enjoyment_compassion'), ('sadness_lonely', 'sadness_lonely'), ('sadness_heartbroken', 'sadness_heartbroken'), ('sadness_gloomy', 'sadness_gloomy'), ('sadness_disappointed', 'sadness_disappointed'), ('sadness_hopeless', 'sadness_hopeless'), ('sadness_grieved', 'sadness_grieved'), ('sadness_unhappy', 'sadness_unhappy'), ('sadness_lost', 'sadness_lost'), ('sadness_troubled', 'sadness_troubled'), ('sadness_resigned', 'sadness_resigned'), ('sadness_miserable', 'sadness_miserable'), ('fear_worried', 'fear_worried'), ('fear_doubtful', 'fear_doubtful'), ('fear_nervous', 'fear_nervous'), ('fear_anxious', 'fear_anxious'), ('fear_terrified', 'fear_terrified'), ('fear_panicked', 'fear_panicked'), ('fear_horrified', 'fear_horrified'), ('fear_desperate', 'fear_desperate'), ('fear_confused', 'fear_confused'), ('fear_stressed', 'fear_stressed'), ('anger_annoyed', 'anger_annoyed'), ('anger_frustrated', 'anger_frustrated'), ('anger_peeved', 'anger_peeved'), ('anger_contrary', 'anger_contrary'), ('anger_bitter', 'anger_bitter'), ('anger_infuriated', 'anger_infuriated'), ('anger_irritated', 'anger_irritated'), ('anger_mad', 'anger_mad'), ('anger_cheated', 'anger_cheated'), ('anger_vengeful', 'anger_vengeful'), ('anger_insulted', 'anger_insulted'), ('disgust_dislike', 'disgust_dislike'), ('disgust_revulsion', 'disgust_revulsion'), ('disgust_loathing', 'disgust_loathing'), ('disgust_disapproving', 'disgust_disapproving'), ('disgust_offended', 'disgust_offended'), ('disgust_horrified', 'disgust_horrified'), ('disgust_uncomfortable', 'disgust_uncomfortable'), ('disgust_nauseated', 'disgust_nauseated'), ('disgust_disturbed', 'disgust_disturbed'), ('disgust_withdrawal', 'disgust_withdrawal'), ('disgust_aversion', 'disgust_aversion')], max_length=64)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Feeling',
        ),
    ]

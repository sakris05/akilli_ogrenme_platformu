# Generated by Django 2.0.3 on 2018-04-11 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_review_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='wine',
            name='genres',
            field=models.CharField(default='unspecified', max_length=200),
        ),
        migrations.AlterField(
            model_name='review',
            name='user_id',
            field=models.IntegerField(default=943),
        ),
    ]

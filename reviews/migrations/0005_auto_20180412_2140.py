# Generated by Django 2.0.3 on 2018-04-12 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20180411_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fake',
            fields=[
                ('actual_id', models.IntegerField(default=6045)),
                ('fake_id', models.AutoField(default=944, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterField(
            model_name='review',
            name='user_id',
            field=models.IntegerField(default=944),
        ),
    ]
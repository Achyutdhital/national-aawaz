# Generated by Django 4.2.6 on 2023-10-18 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adsImg', models.ImageField(upload_to='ads/')),
                ('title', models.CharField(max_length=500)),
            ],
        ),
    ]

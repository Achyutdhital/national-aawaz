# Generated by Django 4.2.6 on 2023-10-18 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_news_create_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoUrl', models.URLField(max_length=1000)),
                ('title', models.CharField(max_length=500)),
            ],
        ),
    ]
# Generated by Django 4.2.6 on 2023-10-13 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_news_highlight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='create_date',
            field=models.CharField(default='(२०८०-आश्विन-शुक्रबार)', editable=False, max_length=50),
        ),
    ]

# Generated by Django 5.2.1 on 2025-06-15 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_seasonalpromotion'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='sent_as_newsletter',
            field=models.BooleanField(default=False, help_text='Has this post already been sent as a newsletter?'),
        ),
    ]

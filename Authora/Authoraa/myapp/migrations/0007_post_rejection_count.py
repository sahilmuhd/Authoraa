# Generated by Django 5.0.2 on 2025-07-22 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rejection_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

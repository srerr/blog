# Generated by Django 4.1.7 on 2023-03-12 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_tag_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='view_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
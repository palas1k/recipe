# Generated by Django 4.2.3 on 2023-10-31 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_count_comments_alter_post_count_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='count_likes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

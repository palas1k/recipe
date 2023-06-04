# Generated by Django 4.1.5 on 2023-06-04 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0003_delete_follower'),
        ('post_create', '0002_remove_post_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(max_length=600, verbose_name='Текст комментария')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.profile')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_post', to='post_create.post')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(max_length=600, verbose_name='Ответ на комментарий')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.profile')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_comments', to='comments_answers.comments')),
            ],
        ),
    ]

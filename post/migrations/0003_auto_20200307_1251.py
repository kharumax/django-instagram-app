# Generated by Django 2.2.7 on 2020-03-07 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_hash'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='target',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='target',
            new_name='post',
        ),
        migrations.RemoveField(
            model_name='like',
            name='like',
        ),
    ]
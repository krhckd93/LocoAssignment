# Generated by Django 2.0.4 on 2018-04-28 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_auto_20180428_2157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_id',
            new_name='parent_comment_id',
        ),
    ]

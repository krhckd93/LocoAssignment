# Generated by Django 2.0.4 on 2018-04-28 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20180428_0556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_id',
            field=models.ForeignKey(db_column='parent_comment_id', on_delete=django.db.models.deletion.CASCADE, to='comments.Comment'),
        ),
    ]
# Generated by Django 2.0.4 on 2018-04-29 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_auto_20180429_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent_comment_id',
            field=models.ForeignKey(blank=True, db_column='parent_comment_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.Comment'),
        ),
    ]

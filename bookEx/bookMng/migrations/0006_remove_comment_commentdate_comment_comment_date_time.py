# Generated by Django 5.1.3 on 2024-11-28 02:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookMng", "0005_comment_commentdate"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="commentdate",
        ),
        migrations.AddField(
            model_name="comment",
            name="comment_date_time",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
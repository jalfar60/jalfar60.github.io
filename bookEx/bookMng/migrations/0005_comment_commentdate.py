# Generated by Django 5.1.3 on 2024-11-28 01:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookMng", "0004_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="commentdate",
            field=models.DateField(auto_now=True),
        ),
    ]

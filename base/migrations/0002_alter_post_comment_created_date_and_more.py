# Generated by Django 4.1.2 on 2022-11-29 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post_comment",
            name="created_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="post_like",
            name="created_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="user_post",
            name="created_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

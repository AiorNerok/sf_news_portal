# Generated by Django 4.1.5 on 2023-01-09 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

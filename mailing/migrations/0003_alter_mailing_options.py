# Generated by Django 4.2.2 on 2024-09-18 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0002_alter_mailing_next_send_time"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mailing",
            options={"verbose_name": "Рассылка", "verbose_name_plural": "Рассылки"},
        ),
    ]

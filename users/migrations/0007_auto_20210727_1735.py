# Generated by Django 3.1.2 on 2021-07-27 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_contact_chat_bot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='telegram',
            field=models.CharField(max_length=150, null=True, verbose_name='Telegram'),
        ),
    ]

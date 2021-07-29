# Generated by Django 3.1.2 on 2021-07-23 19:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.IntegerField(primary_key=True, serialize=False)),
                ('order_type', models.CharField(choices=[('R', 'Repair'), ('M', 'Maintenance'), ('C', 'Consultation')], max_length=1)),
                ('status', models.CharField(choices=[('D', 'DONE'), ('P', 'IN_PROGRESS'), ('N', 'NEW')], default='N', max_length=1)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
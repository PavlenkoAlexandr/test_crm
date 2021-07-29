# Generated by Django 3.1.2 on 2021-07-24 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0002_auto_20210723_2259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='worker_id',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='OrderWorker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='orders.order')),
                ('worker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
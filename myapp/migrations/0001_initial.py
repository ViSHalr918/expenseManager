# Generated by Django 5.0.7 on 2024-08-08 03:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('budget', models.PositiveIntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('amount', models.PositiveIntegerField()),
                ('payment_method', models.CharField(choices=[('cash', 'cash'), ('upi', 'upi'), ('card', 'card')], default='cash', max_length=200)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('category_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

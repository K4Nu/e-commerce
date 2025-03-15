# Generated by Django 5.1.7 on 2025-03-15 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='products.category')),
            ],
            options={
                'ordering': ['name'],
                'indexes': [models.Index(fields=['category_id', 'name'], name='category_size')],
            },
        ),
    ]

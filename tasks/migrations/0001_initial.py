# Generated by Django 5.0.7 on 2024-07-26 18:38

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
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PL', 'PLANNED'), ('RE', 'REVIEW'), ('IP', 'IN_PROGRESS'), ('DN', 'DONE')], default='PL', max_length=10)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('done', models.DateTimeField(blank=True, null=True)),
                ('scheduled', models.DateTimeField()),
                ('assigned', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
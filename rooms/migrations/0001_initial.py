# Generated by Django 5.0.6 on 2024-05-17 06:26

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
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(default='', max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('coutry', models.CharField(default='Korea', max_length=50)),
                ('city', models.CharField(default='Seoul', max_length=80)),
                ('price', models.PositiveIntegerField()),
                ('rooms', models.PositiveIntegerField()),
                ('toilets', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=250)),
                ('pet_friendly', models.BooleanField(default=False)),
                ('kind', models.CharField(choices=[('entire_place', 'Entire Place'), ('private_room', 'Private Room'), ('shared_room', 'Shared Room')], max_length=20)),
                ('amenities', models.ManyToManyField(to='rooms.amenity')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

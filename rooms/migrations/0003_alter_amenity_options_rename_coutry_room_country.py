# Generated by Django 5.0.6 on 2024-05-17 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_room_delete_rooms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amenity',
            options={'verbose_name_plural': 'Amenities'},
        ),
        migrations.RenameField(
            model_name='room',
            old_name='coutry',
            new_name='country',
        ),
    ]

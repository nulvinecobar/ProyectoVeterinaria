# Generated by Django 4.1.3 on 2024-09-07 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VETTORRES', '0013_contacto_fecha_fecha'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contacto',
            old_name='fecha_fecha',
            new_name='fecha_contacto',
        ),
    ]

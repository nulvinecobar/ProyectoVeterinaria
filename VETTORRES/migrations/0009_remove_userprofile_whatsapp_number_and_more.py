# Generated by Django 4.1.3 on 2024-09-02 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VETTORRES', '0008_cita_cancelada_cita_confirmada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='whatsapp_number',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]

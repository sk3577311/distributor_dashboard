# Generated by Django 4.2.18 on 2025-01-24 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_rename_commsion_transaction_commision'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='commision',
            new_name='commission',
        ),
    ]

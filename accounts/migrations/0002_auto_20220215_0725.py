# Generated by Django 3.1 on 2022-02-15 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='date_joind',
            new_name='date_joined',
        ),
        migrations.RenameField(
            model_name='account',
            old_name='fisrt_name',
            new_name='first_name',
        ),
    ]
# Generated by Django 2.0 on 2019-07-12 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0009_auto_20190712_1518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostmodel',
            old_name='account',
            new_name='username',
        ),
    ]

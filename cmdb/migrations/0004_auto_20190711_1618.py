# Generated by Django 2.0 on 2019-07-11 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0003_auto_20190711_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostmodel',
            name='hostname',
            field=models.CharField(blank=True, max_length=50, verbose_name='主机名'),
        ),
    ]

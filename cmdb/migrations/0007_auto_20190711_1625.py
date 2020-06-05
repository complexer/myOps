# Generated by Django 2.0 on 2019-07-11 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0006_auto_20190711_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostmodel',
            name='asset_no',
        ),
        migrations.RemoveField(
            model_name='hostmodel',
            name='asset_type',
        ),
        migrations.AddField(
            model_name='hostmodel',
            name='host_type',
            field=models.CharField(blank=True, choices=[('1', '物理机'), ('2', '虚拟机'), ('3', '容器'), ('4', '云主机')], max_length=30, null=True, verbose_name='主机类型'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='account',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='账号'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='cpu_model',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='CPU型号'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='cpu_num',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='CPU数量'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='disk',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='硬盘信息'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='environment',
            field=models.CharField(blank=True, choices=[('1', '开发环境'), ('2', '测试环境'), ('3', '预发布环境'), ('4', '生产环境')], max_length=32, null=True, verbose_name='环境'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='mac',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='mac地址'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='memory',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='内存大小'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='os',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='操作系统'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='other_ip',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='其它IP'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='password',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='position',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='所在位置'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='remarks',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='备注信息'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='sn',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='SN号码'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='up_time',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='上架时间'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='hostmodel',
            name='vendor',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='设备厂商'),
        ),
    ]
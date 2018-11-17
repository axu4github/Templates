# Generated by Django 2.1.2 on 2018-11-13 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20181113_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='租户名称')),
                ('code', models.CharField(max_length=255, verbose_name='租户代码')),
                ('status', models.CharField(max_length=20, verbose_name='租户状态')),
                ('type', models.CharField(max_length=255, verbose_name='租户类型')),
                ('details', models.TextField(default='', verbose_name='租户详情')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='租户创建时间')),
                ('modified', models.DateTimeField(auto_now_add=True, verbose_name='租户修改时间')),
            ],
        ),
    ]
# Generated by Django 2.1.2 on 2018-11-28 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='tenant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.Tenant'),
            preserve_default=False,
        ),
    ]

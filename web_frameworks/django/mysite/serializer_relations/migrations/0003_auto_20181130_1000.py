# Generated by Django 2.1.2 on 2018-11-30 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serializer_relations', '0002_auto_20181130_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='album',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='serializer_relations.Album'),
        ),
    ]
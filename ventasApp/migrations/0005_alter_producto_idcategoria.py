# Generated by Django 5.2.1 on 2025-06-18 04:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventasApp', '0004_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='idcategoria',
            field=models.ForeignKey(db_column='idcategoria', on_delete=django.db.models.deletion.CASCADE, to='ventasApp.categoria'),
        ),
    ]

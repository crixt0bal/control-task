# Generated by Django 3.0.4 on 2022-09-16 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20220915_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cargo_empleado',
            field=models.ForeignKey(db_column='cargo_empleado', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.CargoEmpleado'),
        ),
    ]
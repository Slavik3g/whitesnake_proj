# Generated by Django 4.2.3 on 2023-07-13 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('carshowroom', '0001_initial'),
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carshowroomsupplierpurchasehistory',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.carmodel'),
        ),
        migrations.AddField(
            model_name='carshowroomsupplierpurchasehistory',
            name='car_showroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='carshowroom.carshowroommodel'),
        ),
        migrations.AddField(
            model_name='carshowroomsupplierpurchasehistory',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='suppliers.suppliermodel'),
        ),
        migrations.AddField(
            model_name='carshowroommodel',
            name='car_list',
            field=models.ManyToManyField(through='carshowroom.CarShowroomCar', to='core.carmodel'),
        ),
        migrations.AddField(
            model_name='carshowroomdiscount',
            name='car_model',
            field=models.ManyToManyField(to='core.carmodel'),
        ),
        migrations.AddField(
            model_name='carshowroomdiscount',
            name='car_showroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='carshowroom.carshowroommodel'),
        ),
        migrations.AddField(
            model_name='carshowroomcar',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.carmodel'),
        ),
        migrations.AddField(
            model_name='carshowroomcar',
            name='car_showroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='carshowroom.carshowroommodel'),
        ),
    ]

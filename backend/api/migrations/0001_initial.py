# Generated by Django 3.2.16 on 2022-12-09 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iata_code', models.CharField(max_length=3, unique=True)),
                ('city', models.CharField(max_length=40)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lon', models.DecimalField(decimal_places=6, max_digits=9)),
                ('state', models.CharField(max_length=2)),
                ('status', models.CharField(choices=[('A', 'Active'), ('I', 'Inactive')], default='A', max_length=1)),
                ('reason', models.TextField(default='')),
            ],
        ),
    ]

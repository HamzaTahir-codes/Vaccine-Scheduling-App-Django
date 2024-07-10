# Generated by Django 5.0.6 on 2024-07-10 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Vaccine Name')),
                ('description', models.TextField(max_length=1024)),
                ('no_of_doses', models.IntegerField(default=1)),
                ('interval', models.IntegerField(default=1, help_text='Please Provide Interval In Days')),
                ('storage_temprature', models.IntegerField(blank=True, help_text='Provide Temp in Celcius', null=True)),
                ('minimum_age', models.IntegerField(default=0)),
            ],
        ),
    ]

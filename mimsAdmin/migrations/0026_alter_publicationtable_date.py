# Generated by Django 3.2.8 on 2021-11-17 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mimsAdmin', '0025_alter_publicationtable_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationtable',
            name='Date',
            field=models.DateTimeField(),
        ),
    ]

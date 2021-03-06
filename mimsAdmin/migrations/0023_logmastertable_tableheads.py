# Generated by Django 3.2.8 on 2021-11-16 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mimsAdmin', '0022_auto_20211116_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='tableHeads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heads', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tableHeads',
            },
        ),
        migrations.CreateModel(
            name='LogMasterTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('TableHeads', models.ManyToManyField(to='mimsAdmin.tableHeads', verbose_name='Table Heads')),
            ],
            options={
                'db_table': 'LogMasterTable',
            },
        ),
    ]

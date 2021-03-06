# Generated by Django 3.2.8 on 2021-11-16 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mimsAdmin', '0020_auto_20211116_1132'),
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
        migrations.AlterUniqueTogether(
            name='bookstable',
            unique_together={('Books_Name', 'Auther_Name', 'Books_Edition')},
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

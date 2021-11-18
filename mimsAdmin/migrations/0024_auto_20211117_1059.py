# Generated by Django 3.2.8 on 2021-11-17 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mimsAdmin', '0023_logmastertable_tableheads'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logmastertable',
            name='status',
            field=models.CharField(choices=[('active', 'Activate'), ('inactive', 'Inactivate')], default='active', max_length=100),
        ),
        migrations.CreateModel(
            name='PublicationTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Publication_Title', models.CharField(max_length=100)),
                ('Volume', models.IntegerField()),
                ('Publication_Author', models.CharField(max_length=100)),
                ('issue', models.CharField(max_length=100)),
                ('Publisher_name', models.CharField(max_length=100)),
                ('Website_Id', models.CharField(max_length=100)),
                ('Journal', models.CharField(max_length=100)),
                ('Date', models.DateField(max_length=100)),
                ('status', models.CharField(choices=[('active', 'Activate'), ('inactive', 'Inactivate')], default='active', max_length=100)),
            ],
            options={
                'db_table': 'PublicationTable',
                'unique_together': {('Publication_Title', 'Volume', 'Publication_Author')},
            },
        ),
    ]

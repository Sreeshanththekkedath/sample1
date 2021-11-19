# Generated by Django 3.2.8 on 2021-11-18 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mimsAdmin', '0032_auto_20211118_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formtable',
            name='status',
            field=models.CharField(choices=[('active', 'Activate'), ('inactive', 'Inactivate')], default='active', max_length=100),
        ),
        migrations.CreateModel(
            name='NotificationTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Notification_Title', models.CharField(max_length=100)),
                ('Details', models.TextField()),
                ('Date', models.DateField()),
                ('status', models.CharField(choices=[('active', 'Activate'), ('inactive', 'Inactivate')], default='active', max_length=100)),
                ('Department', models.ManyToManyField(to='mimsAdmin.department', verbose_name='Departments')),
            ],
            options={
                'db_table': 'Notifications',
            },
        ),
    ]
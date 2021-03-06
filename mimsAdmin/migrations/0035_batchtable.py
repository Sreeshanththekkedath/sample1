# Generated by Django 3.2.8 on 2021-11-19 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mimsAdmin', '0034_notificationtable_added_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Batch_Name', models.CharField(max_length=100)),
                ('From_Date', models.DateField()),
                ('Date_To', models.DateField()),
                ('Batch_Status', models.CharField(choices=[('active', 'Activate'), ('inactive', 'Inactivate')], default='active', max_length=100)),
                ('Department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mimsAdmin.department')),
            ],
            options={
                'db_table': 'Batch',
            },
        ),
    ]

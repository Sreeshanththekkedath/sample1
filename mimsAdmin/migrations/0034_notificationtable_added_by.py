# Generated by Django 3.2.8 on 2021-11-18 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mimsAdmin', '0033_auto_20211118_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationtable',
            name='Added_By',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mimsAdmin.usertable'),
            preserve_default=False,
        ),
    ]
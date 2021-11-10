# Generated by Django 3.2.8 on 2021-11-08 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mimsAdmin', '0014_parentpath_path_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='path',
            name='Path',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='path',
            name='SortOrder',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='path',
            name='pathName',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

# Generated by Django 3.2.8 on 2021-11-05 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mimsAdmin', '0011_experience_faculty_professionalqualification'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionalqualification',
            name='NameOfCollege',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]

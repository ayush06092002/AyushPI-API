# Generated by Django 3.2.21 on 2023-09-21 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_medicine'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicine',
            old_name='users',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='medicine',
            name='dispensing_size',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='dosage',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='precautions',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='preferred_use',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='ref_text',
            field=models.CharField(max_length=255),
        ),
    ]

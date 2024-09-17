# Generated by Django 4.1.6 on 2023-02-13 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_productrate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_top',
            new_name='is_banner',
        ),
        migrations.AddField(
            model_name='product',
            name='banner_photo',
            field=models.ImageField(blank=True, null=True, upload_to='banner/'),
        ),
    ]

# Generated by Django 4.1.6 on 2023-02-11 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_role_unique_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='modified_date',
            new_name='modified_at',
        ),
        migrations.RemoveField(
            model_name='role',
            name='quantity_work',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]

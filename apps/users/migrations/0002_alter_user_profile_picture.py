# Generated by Django 4.0.3 on 2022-04-20 22:43

from django.db import migrations, models
import users.models.users


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.users.user_picture_path),
        ),
    ]

# Generated by Django 4.0.5 on 2022-10-04 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_rename_followers_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='default_profile_pic.png', upload_to=''),
        ),
    ]
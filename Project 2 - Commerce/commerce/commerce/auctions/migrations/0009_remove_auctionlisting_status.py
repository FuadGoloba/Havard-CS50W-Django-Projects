# Generated by Django 4.0.5 on 2022-06-30 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auctionstatus_alter_auctionlisting_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='status',
        ),
    ]
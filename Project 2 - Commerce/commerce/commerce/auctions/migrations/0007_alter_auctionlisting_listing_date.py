# Generated by Django 4.0.5 on 2022-06-30 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auctionlisting_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='listing_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

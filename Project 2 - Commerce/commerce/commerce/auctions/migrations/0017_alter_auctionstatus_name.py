# Generated by Django 4.0.5 on 2022-06-30 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_alter_auctionlisting_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionstatus',
            name='name',
            field=models.CharField(max_length=6),
        ),
    ]

# Generated by Django 4.2.7 on 2024-11-30 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_created_at_listing_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchers', to='auctions.listing'),
        ),
    ]

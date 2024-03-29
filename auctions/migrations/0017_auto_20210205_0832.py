# Generated by Django 3.1.4 on 2021-02-05 08:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20210205_0619'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ManyToManyField(to='auctions.Auction'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='item',
            field=models.ManyToManyField(related_name='watched', to='auctions.Auction'),
        ),
    ]

# Generated by Django 4.1.4 on 2023-01-10 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_categorie_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]

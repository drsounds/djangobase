# Generated by Django 4.1.1 on 2023-03-25 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobase', '0012_alter_collection_options_alter_columngroup_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='columns',
            field=models.ManyToManyField(blank=True, related_name='collections', through='djangobase.CollectionColumnRelation', to='djangobase.column', verbose_name='Columns'),
        ),
    ]

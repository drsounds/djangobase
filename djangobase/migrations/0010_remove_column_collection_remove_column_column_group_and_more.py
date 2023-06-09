# Generated by Django 4.1.1 on 2023-03-19 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobase', '0009_djangoform_feature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='column',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='column',
            name='column_group',
        ),
        migrations.RemoveField(
            model_name='columngroup',
            name='collection',
        ),
        migrations.AddField(
            model_name='column',
            name='column_groups',
            field=models.ManyToManyField(blank=True, related_name='columns', to='djangobase.columngroup'),
        ),
        migrations.AddField(
            model_name='columngroup',
            name='collections',
            field=models.ManyToManyField(blank=True, related_name='column_groups', to='djangobase.collection'),
        ),
        migrations.AlterField(
            model_name='column',
            name='collections',
            field=models.ManyToManyField(blank=True, related_name='columns', to='djangobase.collection'),
        ),
    ]

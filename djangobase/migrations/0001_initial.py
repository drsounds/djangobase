# Generated by Django 4.1.1 on 2023-03-03 08:37

import datetime
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('identifier', models.CharField(blank=True, max_length=255, null=True)),
                ('identifier_type', models.CharField(blank=True, max_length=255, null=True)),
                ('external_id', models.CharField(blank=True, max_length=255, null=True)),
                ('external_id_type', models.CharField(blank=True, max_length=255, null=True)),
                ('old_id', models.CharField(blank=True, max_length=255, null=True)),
                ('guid', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('published', models.DateTimeField(blank=True, null=True)),
                ('unpublished', models.DateTimeField(blank=True, default=datetime.datetime(2099, 12, 31, 0, 0), null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('image_url', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('header_image_url', models.CharField(blank=True, max_length=255, null=True)),
                ('header_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('color_hex', models.CharField(default='rgba(127, 127, 127, .5)', max_length=255)),
                ('background_color_hex', models.CharField(default='transparent', max_length=255)),
                ('tint_color_hex', models.CharField(default='rgba(127,127,127, .5)', max_length=255)),
                ('primary_color_hex', models.CharField(default='rgba(127,127,127, .5)', max_length=255)),
                ('popularity', models.FloatField(default=0)),
                ('streams', models.FloatField(default=0)),
                ('followers', models.FloatField(default=0)),
                ('consumers', models.FloatField(default=0)),
                ('consumes', models.FloatField(default=0)),
                ('external_url', models.URLField(blank=True, null=True)),
                ('sub_type', models.CharField(blank=True, max_length=255, null=True)),
                ('model', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

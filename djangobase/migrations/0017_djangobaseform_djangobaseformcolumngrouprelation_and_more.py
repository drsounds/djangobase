# Generated by Django 4.1.1 on 2023-04-07 13:34

import adminsortable.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        (
            "djangobase",
            "0016_websitefeaturerelation_featurecollectionrelation_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="DjangobaseForm",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("identifier", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "identifier_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "external_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "external_id_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("old_id", models.CharField(blank=True, max_length=255, null=True)),
                ("guid", models.CharField(blank=True, max_length=255, null=True)),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated", models.DateTimeField(default=django.utils.timezone.now)),
                ("deleted", models.DateTimeField(blank=True, null=True)),
                ("published", models.DateTimeField(blank=True, null=True)),
                (
                    "unpublished",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime(2099, 12, 31, 0, 0),
                        null=True,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("summary", models.TextField(blank=True, null=True)),
                ("slug", models.SlugField(blank=True, null=True)),
                ("image_url", models.CharField(blank=True, max_length=255, null=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "header_image_url",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "header_image",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                (
                    "color_hex",
                    models.CharField(default="rgba(127, 127, 127, .5)", max_length=255),
                ),
                (
                    "background_color_hex",
                    models.CharField(default="transparent", max_length=255),
                ),
                (
                    "tint_color_hex",
                    models.CharField(default="rgba(127,127,127, .5)", max_length=255),
                ),
                (
                    "primary_color_hex",
                    models.CharField(default="rgba(127,127,127, .5)", max_length=255),
                ),
                ("popularity", models.FloatField(default=0)),
                ("streams", models.FloatField(default=0)),
                ("followers", models.FloatField(default=0)),
                ("consumers", models.FloatField(default=0)),
                ("consumes", models.FloatField(default=0)),
                ("external_url", models.URLField(blank=True, null=True)),
                ("sub_type", models.CharField(blank=True, max_length=255, null=True)),
                ("class_name", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DjangobaseFormColumnGroupRelation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "column_group_order",
                    models.PositiveIntegerField(
                        db_index=True, default=0, editable=False
                    ),
                ),
            ],
            options={
                "ordering": ["column_group_order"],
            },
        ),
        migrations.CreateModel(
            name="DjangobaseFormColumnRelation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "column_order",
                    models.PositiveIntegerField(
                        db_index=True, default=0, editable=False
                    ),
                ),
            ],
            options={
                "ordering": ["column_order"],
            },
        ),
        migrations.CreateModel(
            name="ExternalIdentifier",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("slug", models.CharField(max_length=255)),
                (
                    "external_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "external_id_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("old_id", models.CharField(blank=True, max_length=255, null=True)),
                ("guid", models.CharField(blank=True, max_length=255, null=True)),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated", models.DateTimeField(default=django.utils.timezone.now)),
                ("deleted", models.DateTimeField(blank=True, null=True)),
                ("published", models.DateTimeField(blank=True, null=True)),
                (
                    "unpublished",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime(2099, 12, 31, 0, 0),
                        null=True,
                    ),
                ),
                ("node_type", models.CharField(blank=True, max_length=255, null=True)),
                ("node_id", models.UUIDField(blank=True, null=True)),
                ("node_slug", models.CharField(blank=True, max_length=255, null=True)),
                ("node_uri", models.CharField(blank=True, max_length=255, null=True)),
                ("identifier", models.CharField(max_length=255)),
                ("identifier_type", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("identifier", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "identifier_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "external_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "external_id_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("old_id", models.CharField(blank=True, max_length=255, null=True)),
                ("guid", models.CharField(blank=True, max_length=255, null=True)),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated", models.DateTimeField(default=django.utils.timezone.now)),
                ("deleted", models.DateTimeField(blank=True, null=True)),
                ("published", models.DateTimeField(blank=True, null=True)),
                (
                    "unpublished",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime(2099, 12, 31, 0, 0),
                        null=True,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("summary", models.TextField(blank=True, null=True)),
                ("slug", models.SlugField(blank=True, null=True)),
                ("image_url", models.CharField(blank=True, max_length=255, null=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "header_image_url",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "header_image",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                (
                    "color_hex",
                    models.CharField(default="rgba(127, 127, 127, .5)", max_length=255),
                ),
                (
                    "background_color_hex",
                    models.CharField(default="transparent", max_length=255),
                ),
                (
                    "tint_color_hex",
                    models.CharField(default="rgba(127,127,127, .5)", max_length=255),
                ),
                (
                    "primary_color_hex",
                    models.CharField(default="rgba(127,127,127, .5)", max_length=255),
                ),
                ("popularity", models.FloatField(default=0)),
                ("streams", models.FloatField(default=0)),
                ("followers", models.FloatField(default=0)),
                ("consumers", models.FloatField(default=0)),
                ("consumes", models.FloatField(default=0)),
                ("external_url", models.URLField(blank=True, null=True)),
                ("sub_type", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ServiceIdentifier",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("slug", models.CharField(max_length=255)),
                (
                    "identifier_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "external_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "external_id_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("old_id", models.CharField(blank=True, max_length=255, null=True)),
                ("guid", models.CharField(blank=True, max_length=255, null=True)),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated", models.DateTimeField(default=django.utils.timezone.now)),
                ("deleted", models.DateTimeField(blank=True, null=True)),
                ("published", models.DateTimeField(blank=True, null=True)),
                (
                    "unpublished",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime(2099, 12, 31, 0, 0),
                        null=True,
                    ),
                ),
                ("node_type", models.CharField(blank=True, max_length=255, null=True)),
                ("node_id", models.UUIDField(blank=True, null=True)),
                ("node_slug", models.CharField(blank=True, max_length=255, null=True)),
                ("node_uri", models.CharField(blank=True, max_length=255, null=True)),
                ("identifier", models.CharField(max_length=255)),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="identifiers",
                        to="djangobase.service",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("identifier", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "identifier_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "external_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "external_id_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("old_id", models.CharField(blank=True, max_length=255, null=True)),
                ("guid", models.CharField(blank=True, max_length=255, null=True)),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated", models.DateTimeField(default=django.utils.timezone.now)),
                ("deleted", models.DateTimeField(blank=True, null=True)),
                ("published", models.DateTimeField(blank=True, null=True)),
                (
                    "unpublished",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime(2099, 12, 31, 0, 0),
                        null=True,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("summary", models.TextField(blank=True, null=True)),
                ("slug", models.SlugField(blank=True, null=True)),
                ("image_url", models.CharField(blank=True, max_length=255, null=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "header_image_url",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "header_image",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                (
                    "color_hex",
                    models.CharField(default="rgba(127, 127, 127, .5)", max_length=255),
                ),
                (
                    "background_color_hex",
                    models.CharField(default="transparent", max_length=255),
                ),
                (
                    "tint_color_hex",
                    models.CharField(default="rgba(127,127,127, .5)", max_length=255),
                ),
                (
                    "primary_color_hex",
                    models.CharField(default="rgba(127,127,127, .5)", max_length=255),
                ),
                ("popularity", models.FloatField(default=0)),
                ("streams", models.FloatField(default=0)),
                ("followers", models.FloatField(default=0)),
                ("consumers", models.FloatField(default=0)),
                ("consumes", models.FloatField(default=0)),
                ("external_url", models.URLField(blank=True, null=True)),
                ("sub_type", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.DeleteModel(
            name="DjangoForm",
        ),
        migrations.AlterField(
            model_name="collection",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="collectiongroup",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="column",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="columngroup",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="feature",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="website",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="djangobaseformcolumnrelation",
            name="column",
            field=adminsortable.fields.SortableForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="djangobase.column"
            ),
        ),
        migrations.AddField(
            model_name="djangobaseformcolumnrelation",
            name="form",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="djangobase.djangobaseform",
            ),
        ),
        migrations.AddField(
            model_name="djangobaseformcolumngrouprelation",
            name="column_group",
            field=adminsortable.fields.SortableForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="djangobase.columngroup"
            ),
        ),
        migrations.AddField(
            model_name="djangobaseformcolumngrouprelation",
            name="form",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="djangobase.djangobaseform",
            ),
        ),
        migrations.AddField(
            model_name="djangobaseform",
            name="column_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="forms",
                through="djangobase.DjangobaseFormColumnGroupRelation",
                to="djangobase.columngroup",
                verbose_name="Column groups",
            ),
        ),
        migrations.AddField(
            model_name="djangobaseform",
            name="columns",
            field=models.ManyToManyField(
                blank=True,
                related_name="forms",
                through="djangobase.DjangobaseFormColumnRelation",
                to="djangobase.column",
                verbose_name="Columns",
            ),
        ),
    ]

import base64
import datetime
import random
import re
import string
from time import mktime
import uuid
from PIL import Image
import blurhash
from django.conf import settings
from django.db import models

from dateutil import parser 

from django.forms import Form
from django.utils.module_loading import import_string

from django.forms.fields import CharField, URLField

from adminsortable.models import SortableMixin, SortableForeignKey
from django.utils import timezone
import random
import string
from time import mktime
import uuid
from datetime import datetime

import base62
from django.contrib.sites.models import Site
from django.db import models

import sys

if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

import io

from colorthief import ColorThief

from django.conf import settings
from django.db.models import Q

from django.utils import timezone
from django.utils.module_loading import import_string

import matplotlib.image as img
import requests

from colorthief import ColorThief

from django.core import serializers


import re


def to_snakecase(s):
    s = re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()
    return s


def to_camelcase(s):
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)


STATUS_CODES = (
    (100, '100 Planned'),
    (101, '101 Submitted'),
    (101, '109 Processing'),
    (201, '201 Done'),
    (204, '204 Done without result'),
    (209, '209 Overdone'),
    (301, '301 Redirect'),
    (404, '404 Not found'),
    (500, '500 Error'),
    (505, '505 Limbo'),
)


def random_string(str_size = 23, allowed_chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))


class DjangobaseModelMixin(models.Model):
    def to_dict(self, *args, **kwargs):
        obj = super(DjangobaseModelMixin, self).to_dict(*args, **kwargs)
        return dict(
            name=self.name,
            description=self.description,
            summary=self.summary,
            imageUrl=self.image.url if self.image else self.image_url,
            headerImageUrl=self.header_image.url if self.header_image else self.header_image_url,
            colorHex=self.color_hex,
            externalUrls=self.external_url,
            **obj
        )
    
    @classmethod
    def get_collection_id(cls):
        return cls().type

    @property
    def type(self):
        return 'collection'

    def to_data(self, level = 0):
        data = {
            'type': self.type,
            'href': f"/{self.type}/{self.slug}",
            'url': f"{settings.DJANGOBASE_OPEN_URL}/{self.type}/{self.slug}",
            'uri': f"{settings.DJANGOBASE_URI_PROTOCOL}:{self.type}:{self.slug}",
            "id": str(self.id)
        }
        fields = self._meta.get_fields(include_hidden=True)
        for field in fields:
            value = None
            field_id = field.name
            if isinstance(field, models.UUIDField):
                value = str(getattr(self, field_id))
            elif isinstance(field, models.ManyToManyField):
                related_objects = getattr(self, field_id)
                value = []
                for related_object in related_objects.all():
                    if hasattr(related_object, 'to_data'):
                        value.append(
                            related_object.to_data(level + 1)
                        ) 
            elif isinstance(field, models.ForeignKey):
                related_object = getattr(self, field_id)
                if related_object:
                    if hasattr(related_object, 'to_data'):
                        value = related_object.to_data(level + 1)
            elif isinstance(field, float):
                try:
                    value = getattr(self, field_id)
                except AttributeError:
                    pass
            elif isinstance(field, models.DateField):
                try:
                    value = getattr(self, field_id)
                    value = value.strftime("%Y-%m-%d %H:%m:%d")
                except AttributeError:
                    pass
            elif isinstance(field, models.DateTimeField):
                try:
                    value = getattr(self, field_id)
                except AttributeError:
                    pass
            elif isinstance(field, models.IntegerField):
                try:
                    value = getattr(self, field_id)
                except AttributeError:
                    pass
            elif isinstance(field, models.CharField):
                try:
                    value = getattr(self, field_id)
                except AttributeError:
                    pass
            elif isinstance(field, models.TextField):
                try:
                    value = getattr(self, field_id)
                except AttributeError:
                    pass
            else:
                continue
            data[to_camelcase(field_id)] = value
        return data

    @classmethod
    def upsert_from_data(cls, user, data, level = 0, *args, **kwargs):
        slug = data.get('slug', None)
        new_node = None
        created = True
        if slug:
            print("Found slug")
            new_node = cls.objects.filter(
                slug=slug
            ).first()
            print("Found existing node")
            print(new_node)
            created = False

        if not user.is_superuser:
            if not hasattr(new_node, 'user'):
                raise Exception("Cant update node")
            if new_node.user.id != new_node.user.id:
                raise Exception("Cant someone else's node")

        fields = cls._meta.get_fields(include_hidden=True)

        row = {}

        for field in fields:
            field_id = field.name

            value = None

            input_field_id = to_snakecase(field_id)
            
            if input_field_id not in data:
                continue

            input_value = data.get(input_field_id, None)
            if isinstance(field, models.OneToOneField):
                if input_value:
                    if hasattr(field.related_model, 'upsert_from_data'):
                        value = field.related_model.upsert_from_data(
                            user,
                            input_value,
                            level + 1
                        )
                        row[field_id] = value
                else:
                        row[field_id] = None
            elif isinstance(field, models.DateTimeField):
                if isinstance(input_value, str):
                    if input_value:
                        date = parser.parse(input_value)
                        row[field_id] = date
                elif isinstance(input_value, int):
                    date = mktime(input_value)
                    row[field_id] = date
                elif isinstance(input_value, datetime):
                    row[field_id] = date
            elif isinstance(field, models.ForeignKey):
                if input_value:
                    if hasattr(field.related_model, 'upsert_from_data'):
                        value = field.related_model.upsert_from_data(
                            user,
                            input_value,
                            level + 1
                        )
                        row[field_id] = value
                else:
                    row[field_id] = None
            elif isinstance(field, models.ManyToManyField):
                if isinstance(input_value, list):
                    associated_objects = []
                    for val in input_value:
                        if hasattr(field.related_model, 'upsert_from_data'):
                            obj = field.related_model.upsert_from_data(
                                user,
                                val,
                                level + 1
                            )
                            associated_objects.append(obj)

                    getattr(new_node, field_id).set(
                        associated_objects
                    )
                else:
                    row[field_id] = None
            elif isinstance(field, models.CharField) or isinstance(field, models.TextField):
                if isinstance(input_value, str):
                    row[field_id] = input_value
            elif isinstance(field, models.IntegerField):
                if isinstance(input_value, int):
                    row[field_id] = input_value
            elif isinstance(field, models.FloatField):
                if isinstance(input_value, int) or isinstance(value, float):
                    row[field_id] = input_value
            else:
                row[field_id] = value
        
        row["user_id"] = user.id

        if new_node:
            for field_id in row.keys():
                if field_id == "id":
                    continue
                setattr(new_node, field_id, row[field_id])
        else:
            print("Creating new object")
            new_node = cls.objects.create(
                **row
            )
            if hasattr(new_node, 'user'):
                new_node.user = user
        new_node.save()
        return new_node
    
    class Meta:
        abstract = True


class Node(DjangobaseModelMixin, models.Model):
    class Meta:
        abstract = True
 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    slug = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    identifier_type = models.CharField(max_length=255, null=True, blank=True)
    external_id = models.CharField(max_length=255, null=True, blank=True)
    external_id_type = models.CharField(max_length=255, null=True, blank=True)
    old_id = models.CharField(max_length=255, null=True, blank=True)
    guid = models.CharField(max_length=255, null=True, blank=True)

    @property
    def type(self):
        return type(self).__name__.lower()

    @property
    def uri(self):
        return f"{settings.DJANGOBASE_URI_PROTOCOL}:{self.type}:{self.slug}"
    
    def to_json(self):
        return dict(
            id=self.id,
            uri=self.uri
        )

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    deleted = models.DateTimeField(null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)
    unpublished = models.DateTimeField(null=True, blank=True, default=datetime(2099,12,31,0,0,0))

    def save(self, *args, **kwargs):
        if not self.identifier or not self.slug:
            if not self.id:
                self.id = uuid.uuid4()
            identifier = base62.encode(int(self.id))
            if not self.identifier:
                self.identifier = identifier
            if not self.slug:
                self.slug = identifier
        super(Node, self).save(*args, **kwargs)

    def to_dict(self, *args, **kwargs):
        return dict(
           id=self.slug
        )
    
    def generate_colors(self, *args, **kwargs):
        pass


class Entity(Node):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_blurhash = models.TextField(null=True, blank=True)
    header_image_url = models.CharField(max_length=255, null=True, blank=True)
    header_image_blurhash = models.TextField(null=True, blank=True)
    header_image = models.ImageField(null=True, blank=True)
    color_hex = models.CharField(max_length=255, default='rgba(127, 127, 127, .5)')
    background_color_hex = models.CharField(max_length=255, default='transparent')
    tint_color_hex = models.CharField(max_length=255, default='rgba(127,127,127, .5)')
    primary_color_hex = models.CharField(max_length=255, default='rgba(127,127,127, .5)')
    popularity = models.FloatField(default=0)
    streams = models.FloatField(default=0)
    followers = models.FloatField(default=0)
    consumers = models.FloatField(default=0)
    consumes = models.FloatField(default=0)
    external_url = models.URLField(null=True, blank=True)
    sub_type = models.CharField(max_length=255, null=True, blank=True)

    @classmethod
    def get_collection_type(cls):
        return cls().type

    @property
    def type(self):
        return 'entity'

    def __str__(self):
        if not self.name:
           return ''
        return self.name

    def save(self, *args, **kwargs):
        super(Entity, self).save(*args, **kwargs)
        self.generate_colors(False)
        self.generate_blurhash_for_images()

    def generate_blurhash_for_image(self, attr_name):
        print(f"Generating blurhash for {attr_name}")
        image_attr_value = getattr(self, attr_name)
        image_attr_url = getattr(self, f"{attr_name}_url")
        print(image_attr_url)
        image_path = image_attr_url
        if not image_path:
            image_path = image_attr_value.url
            print("Getting from url")
        if not image_path:
            print("Image attr is None")
            return
        try:
            print(f"Loading image from '{image_path}'")
            image = None
            if image_path.startswith('http'):
                response = requests.get(image_path)
                image = Image.open(BytesIO(response.content))
                print(image)
            else:
                image = Image.open(image_path)
            if not image:
                print("Image is None")
                raise Exception("Image not loaded properly")
            image.thumbnail(( 100, 100))
            hash = blurhash.encode(image, x_components=4, y_components=2)
            setattr(self, f"{attr_name}_blurhash", hash)
            print(f"Successfully set {attr_name}_blurhash to {hash}")
        except Exception as e:
            print(f"Couldn't load image from '{image_path}'")
            raise e

    def generate_blurhash_for_images(self):
        for image_attr in ['image', 'header_image']:
            self.generate_blurhash_for_image(image_attr)


def resolve_node_type(node_type):
    if node_type in settings.DJANGOBASE_NODE_TYPES:
        node_model = import_string(settings.DJANGOBASE_NODE_TYPES[node_type])
        return node_model


def resolve_node(node_type, node_slug=None, node_id=None):
    node_model = resolve_node_type(node_type)
    if node_model:
        if node_id:
            try:
               obj = node_model.objects.get(id=node_id)
               return obj
            except:
               pass
        if node_slug:
            try:
                obj = node_model.objects.filter(
                    Q(slug=node_slug)
                ).first()
                return obj
            except Exception as e:
                raise e

    raise Exception("Entity type {node_type} not found".format(node_type=node_type))


def generic_query_node(node_type, **kwargs):
    node_model = resolve_node_type(node_type)
    if node_model:
        obj = generic_query(node_model, **kwargs)
        return obj
    raise Exception("Entity type {node_type} not found".format(node_type=node_type))


def get_node_by_uri(uri):
    if uri.startswith(f'{settings.DJANGOBASE_URI_PROTOCOL}:'):
        segments = uri.split(':')
        node_type = segments[1]
        node_slug = segments[2]
        return resolve_node(node_type, node_slug)


def query_node_by_uri(uri, **kwargs):
    if uri.startswith(f'{settings.DJANGOBASE_URI_PROTOCOL}:'):
        segments = uri.split(':')
        node_type = segments[1]
        return generic_query_node(node_type, **kwargs)


def generic_query(model, *args, **kwargs):
    try:
        return model.objects.filter(
            ~Q(published=None),
            Q(Q(unpublished__gte=timezone.now()) | Q(unpublished=None)),
            *args,
            **kwargs
        )
    except Exception as e:
        raise e


def resolve_entify_service_by_uri(uri):
    for service_path in settings.ENTIFY_SERVICES:
        service_klass = import_string(service_path)
        service = service_klass()
        if service.accepts_uri(uri):
            return service
    return None


def resolve_node_by_service_uri(uri):
    service = resolve_entify_service_by_uri(uri)
    if service:
        return service.resolve_node(uri)
    return None


def generic_user_get(model, id, user, *args, **kwargs):
    if user.is_superuser:
        return model.objects.filter(
            Q(
                Q(slug=id)|Q(identifier=id)
            ),
            *args,
            **kwargs
        ).first()
    return model.objects.filter(
        Q(
            Q(
                Q(slug=id)|Q(identifier=id)
            ),
            Q(
                Q(
                    Q(published__isnull=False),
                        Q(Q(unpublished__isnull=True) | Q(unpublished__gte=timezone.now()))
                ) | Q(
                    user=user
                )
            )
        ),
        *args,
        **kwargs
    ).first()


def resolve_node_by_uri(uri):
    if len(uri) > 0 and not uri.startswith(f'{settings.DJANGOBASE_URI_PROTOCOL}:'):
        return resolve_entify_service_by_uri(uri)

    segments = uri.split(":")
    node_type = segments[1]
    node_slug = segments[2]
    return resolve_node(node_type, node_slug)


def generic_get(model, id, *args, **kwargs):
    return model.objects.get(
        Q(
            Q(slug=id)|Q(identifier=id)
        ),
        Q(published__isnull=False),
        Q(deleted__isnull=True),
        Q(Q(unpublished__isnull=True) | Q(unpublished__gte=timezone.now())),
        *args,
        **kwargs
    )


def generic_users_get(model, user, id, *args, **kwargs):
    return model.objects.get(
        Q(
            Q(
                Q(slug=id)|Q(identifier=id)
            ),
            Q(
                Q(
                    Q(published__isnull=False),
                        Q(Q(unpublished__isnull=True) | Q(unpublished__gte=timezone.now()))
                ) | Q(
                    users__in=[user]
                )
            )
        ),
        *args,
        **kwargs
    )


def generic_user_query(model, user, *args, **kwargs):
    if user.is_superuser:
        return model.objects.filter(
            *args,
            **kwargs
        )
    try:
        return model.objects.filter(
            Q(
                Q(
                    Q(published__isnull=False),
                    Q(Q(unpublished__gte=timezone.now()) | Q(unpublished=None))
                ) |
                Q(
                  user=user
                )
            ),
            *args,
            **kwargs
        )
    except Exception as e:
        raise e
        return None


class Service(Entity):
    pass


class ExternalIdentifier(Node):
    node_type = models.CharField(max_length=255, null=True, blank=True)
    node_id = models.UUIDField(blank=True, null=True)
    node_slug = models.CharField(max_length=255, blank=True, null=True)
    node_uri = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(max_length=255)
    identifier_type = models.CharField(max_length=255)

    @property
    def node(self):
        try:
            return resolve_node(
                self.node_type,
                self.node_slug,
                self.node_id
            )
        except Exception as e:
            raise e


class ServiceIdentifier(Node):
    node_type = models.CharField(max_length=255, null=True, blank=True)
    node_id = models.UUIDField(blank=True, null=True)
    node_slug = models.CharField(max_length=255, blank=True, null=True)
    node_uri = models.CharField(max_length=255, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='identifiers')
    identifier = models.CharField(max_length=255)

    @property
    def node(self):
        try:
            return resolve_node(
                self.node_type,
                self.node_slug,
                self.node_id
            )
        except Exception as e:
            raise e


class Column(SortableMixin, Entity):
    class Meta:
        verbose_name = 'Column'
        verbose_name_plural = 'Columns'
        ordering = ['number']

    #collection = models.ForeignKey(Collection, null=True, blank=True, on_delete=models.CASCADE, related_name='columns')
    #column_group = models.ForeignKey(ColumnGroup, null=True, blank=True, on_delete=models.CASCADE, related_name='columns')
  
    column_type = models.CharField(max_length=255, blank=True, default='text')

    foreign_collection = models.ForeignKey('Collection', blank=True, null=True, on_delete=models.CASCADE, related_name='foreign_columns')

    number = models.IntegerField(default=0)

    def to_data(self, level, *args, **kwargs):
        obj = super(Column, self).to_data(level, *args, **kwargs)
        if self.foreign_collection:
            obj['model'] = self.foreign_collection.slug
        return obj

    @property
    def type(self):
        return 'column'


class ColumnGroup(SortableMixin, Entity):
    class Meta:
        verbose_name = 'Column group'
        verbose_name_plural = 'Column groups'
        ordering = ['number']

    #collection = models.ForeignKey(Collection, null=True, on_delete=models.CASCADE, related_name='groups')

    columns = models.ManyToManyField(
        Column,
        through='ColumnGroupColumnRelation',
        through_fields=('column_group', 'column'), 
        verbose_name="Columns",
        blank=True,
        related_name='column_groups'
    )
  
    number = models.IntegerField(default=0)

    def to_data(self, level, *args, **kwargs):
        obj = super(ColumnGroup, self).to_data(level, *args, **kwargs)
        if level < 5:
            obj['columns'] = [
                column.to_data(level + 1, *args, **kwargs)
                for
                column
                in
                self.columns.all()
            ]
        return obj

    @property
    def type(self):
        return 'columnGroup'


class Collection(SortableMixin, Entity):
    class Meta:
        verbose_name = 'Collections'
        verbose_name_plural = 'Collections'
        ordering = ['number']

    model = models.CharField(max_length=255)

    def get_django_model(self):
        django_model = import_string(self.model)
        return django_model

    number = models.IntegerField(default=0)

    column_groups = models.ManyToManyField(
        ColumnGroup,
        through='CollectionColumnGroupRelation',
        through_fields=('collection', 'column_group'), 
        verbose_name="Column groups",
        blank=True,
        related_name='collections'
    )
    
    columns = models.ManyToManyField(
        Column,
        through='CollectionColumnRelation',
        through_fields=('collection', 'column'), 
        verbose_name="Columns",
        blank=True,
        related_name='collections'
    )

    @property
    def type(self):
        return 'model'

    def to_data(self, level = 0, *args, **kwargs):
        
        data = super(Collection, self).to_data(level + 1, *args, **kwargs)
        if level < 5:
            data['columns'] = [
                column.to_data(level + 1)
                for
                column
                in
                self.columns.all()
            ]
            data['columnGroups'] = [
                column_group.to_data(level + 1)
                for
                column_group
                in
                self.column_groups.all()
            ]
        return data


class Feature(Entity):
    collections = models.ManyToManyField(
        Collection,
        blank=True,
        through='FeatureCollectionRelation',
        through_fields=('feature', 'collection'),
        related_name='features'
    )


class Website(Entity):
    domain = models.CharField(max_length=255)
    style = models.JSONField()
    features = models.ManyToManyField(
        Feature,
        through='WebsiteFeatureRelation',
        through_fields=('website', 'feature'),
        verbose_name='features',
        blank=True,
        related_name='websites'
    )

    @property
    def type(self):
        return "site"

    def to_data(self, level, *args, **kwargs):
        obj = super(Website, self).to_data(*args, **kwargs)
        obj['domains'] = self.domain.split(',')
        obj['features'] = [
            f.to_data(level + 1)
            for
            f
            in
            self.features.all()
        ]
        obj['models'] = [
            c.to_data(level + 1)
            for
            c
            in
            Collection.objects.all()
        ]
        return obj
  
    def to_dict(self, level = 0, *args, **kwargs):
        obj = super(Website, self).to_dict(*args, **kwargs)
        obj['style'] = self.style
        obj['domains'] = self.domain.split(',')
        obj['features'] = [
            f.to_data(level + 1)
            for
            f
            in
            self.features.all()
        ]
        obj['models'] = [
            c.to_data()
            for
            c
            in
            Collection.objects.all()
        ]
        return obj


class CollectionGroup(SortableMixin, Entity):
    class Meta:
        ordering = ['number']

    site = models.ForeignKey(Website, on_delete=models.CASCADE, blank=True, null=True)

    collections = models.ManyToManyField(
        Collection,
        through='CollectionGroupCollectionRelation',
        through_fields=('collection_group', 'collection'), 
        verbose_name="Collection groups",
        blank=True,
        related_name='collection_groups'
    )

    number = models.PositiveIntegerField(default=0)


class CollectionGroupCollectionRelation(SortableMixin):
    class Meta:
        ordering = ['collection_order']

    collection_group = models.ForeignKey(CollectionGroup, on_delete=models.CASCADE)
    collection = SortableForeignKey(Collection, on_delete=models.CASCADE)
    collection_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)


class ColumnGroupColumnRelation(SortableMixin):
    class Meta:
        ordering = ['column_order']

    column_group = models.ForeignKey(ColumnGroup, on_delete=models.CASCADE)
    column = SortableForeignKey(Column, on_delete=models.CASCADE)
    column_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)


class CollectionColumnRelation(SortableMixin):
    class Meta:
        ordering = ['column_order']

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    column = SortableForeignKey(Column, on_delete=models.CASCADE)
    column_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)


class CollectionColumnGroupRelation(SortableMixin):
    class Meta:
        ordering = ['column_group_order']

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    column_group = SortableForeignKey(ColumnGroup, on_delete=models.CASCADE)
    column_group_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)


class DjangobaseForm(Entity):
    class_name = models.CharField(max_length=255)

    column_groups = models.ManyToManyField(
        ColumnGroup,
        through='DjangobaseFormColumnGroupRelation',
        through_fields=('form', 'column_group'), 
        verbose_name="Column groups",
        blank=True,
        related_name='forms'
    )

    columns = models.ManyToManyField(
        Column,
        through='DjangobaseFormColumnRelation',
        through_fields=('form', 'column'), 
        verbose_name="Columns",
        blank=True,
        related_name='forms'
    )

    @property
    def type(self):
        return 'form'
    
    def to_data(self, level, *args, **kwargs):
        obj = super(DjangobaseForm, self).to_data(level, *args, **kwargs)
        obj['type'] = 'form'

    @property
    def form_class(self):
        return import_string(self.class_name)

    def get_form_fields(self, request):
        form = self.create_instance(request)
        result = []
        for field_id in form.fields.keys():
            field = form.fields[field_id]
            field_obj = dict(
                type='field',
                slug=field_id,
                name=field.name
            )

            for attr in ['max_length', 'min_length']:
                if hasattr(field, attr):
                    field_obj[attr] = getattr(field, attr)

            if isinstance(field, CharField):
                field_obj['type'] = 'text'
            elif isinstance(field, URLField):
                field_obj['type'] = 'url'

            result.append(
                field_obj
            )

    def create_instance(self, request, *args, **kwargs):
        """
        Creates an instance of the form
        """
        form_class : Form = self.form_class
        form : Form = form_class(
            request=request,
            *args,
            **kwargs
        )
        return form


class DjangobaseFormColumnGroupRelation(SortableMixin):
    class Meta:
        ordering = ['column_group_order']

    form = models.ForeignKey(DjangobaseForm, on_delete=models.CASCADE)
    column_group = SortableForeignKey(ColumnGroup, on_delete=models.CASCADE)
    column_group_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)


class DjangobaseFormColumnRelation(SortableMixin):
    class Meta:
        ordering = ['column_order']

    form = models.ForeignKey(DjangobaseForm, on_delete=models.CASCADE)
    column = SortableForeignKey(Column, on_delete=models.CASCADE)
    column_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)


class WebsiteFeatureRelation(SortableMixin):
    class Meta:
        ordering = ['feature_order']

    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    feature = SortableForeignKey(Feature, on_delete=models.CASCADE)
    feature_order = models.PositiveIntegerField(default=0)


class FeatureCollectionRelation(SortableMixin):
    class Meta:
        ordering = ['collection_order']

    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    collection = SortableForeignKey(Collection, on_delete=models.CASCADE)
    collection_order = models.PositiveIntegerField(default=0)


class Tag(Entity):
    pass

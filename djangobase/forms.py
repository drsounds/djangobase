import datetime
from time import mktime
from typing import Collection
from django.forms import Form

from dateutil import parser
from djangobase.models import to_snakecase
from django import forms


class DjangobaseFormMixin(Form):
    class Meta:
        abstract = True

    def to_data(self):
        result = dict(
            columns=[]
        )
        fields = self._meta.get_fields(include_hidden=True)
        for field in fields:
            field_result = dict(
                slug=field.name,
                name=field.title,
                type='object'
            )
            if field is forms.MultipleChoiceField:
                if field_result.queryset:
                    field_result['type'] = 'belongsToMany'
                    queryset_model = field_result.queryset.model
                    collection_slug = queryset_model.get_collection_id()
                    field_result['model'] = collection_slug
            elif field is forms.IntegerField:
                field_result['type'] = 'number'
            elif field is forms.CharField:
                field_result['type'] = 'text'
            elif field is forms.ChoiceField:
                if field_result.queryset:
                    field_result['type'] = 'belongsTo'
                    queryset_model = field_result.queryset.model
                    collection_slug = queryset_model.get_collection_id()
                    field_result['model'] = collection_slug
            else:
                continue
            
            result['columns'] = field_result
        return result

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
            if isinstance(field, forms.OneToOneField):
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
            elif isinstance(field, forms.DateTimeField):
                if isinstance(input_value, str):
                    if input_value:
                        date = parser.parse(input_value)
                        row[field_id] = date
                elif isinstance(input_value, int):
                    date = mktime(input_value)
                    row[field_id] = date
                elif isinstance(input_value, datetime):
                    row[field_id] = date
            elif isinstance(field, forms.InlineForeignKeyField):
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
            elif isinstance(field, forms.MultipleChoiceField):
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
    
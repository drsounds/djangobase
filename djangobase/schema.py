from django.core.paginator import Paginator
from django.db.models import OuterRef
from django.db.models import Q, Sum

from django.http import HttpRequest, QueryDict

from django.utils.module_loading import import_string
import graphene
from djangobase.models import Collection, ColumnGroup, DjangoForm

from djangobase.models import generic_user_get, generic_user_query

from graphene_django import DjangoObjectType


class DjangobaseDocumentNode(graphene.ObjectType):
    data = graphene.Field(graphene.JSONString)
    slug = graphene.Field(graphene.String)
    id = graphene.Field(graphene.UUID)
    collection = graphene.Field(graphene.String)
    created = graphene.Field(graphene.DateTime)
    updated = graphene.Field(graphene.DateTime)
    published = graphene.Field(graphene.DateTime)

    documents = graphene.List(
        'djangobase.schema.DjangobaseDocumentNode',
        collection_id=graphene.String(required=True),
        filters=graphene.JSONString(required=False),
        p=graphene.Int(required=False),
        size=graphene.Int(required=False)
    )

    def resolve_documents(self, info, collection_id, filters={}, p=0, size=28):
        child_collection = Collection.objects.get(
            slug=collection_id
        )

        filters[f"{self.model}__slug"] = self.slug

        if not child_collection:
            raise Exception("Child collection is None")

        model = import_string(child_collection.model)
        if not model:
            raise Exception(f"Invalid documents {self.model}")
        q = generic_user_query(
            model,
            info.context.user,
            **filters
        )
        paginator = Paginator(
            q,
            size
        ).page(p + 1)
        docs = []
    
        return [
            DjangobaseDocumentNode(
              id=n.id,
              slug=n.slug,
              collection=self,
              data=n.to_data()
            )
            for
            n
            in
            paginator.object_list
        ]


class DjangobaseColumnGroupEntity(DjangoObjectType):
    class Meta:
        model = ColumnGroup
        fields = ['name', 'number']


class DjangobaseCollectionNode(DjangoObjectType):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'slug']

    document = graphene.Field(
        'djangobase.schema.DjangobaseDocumentNode',
        id=graphene.String(required=False),
        slug=graphene.String(required=False)
    )
    documents = graphene.List(
        'djangobase.schema.DjangobaseDocumentNode',
        filters=graphene.JSONString(required=False),
        p=graphene.Int(required=False),
        size=graphene.Int(required=False)
    )
    slug = graphene.Field(graphene.String)
    model = graphene.Field(graphene.String)
    id = graphene.Field(graphene.UUID)

    def resolve_documents(self, info, filters = {}, p = 0, size = 28):
        model = import_string(self.model)
        if not model:
            raise Exception(f"Invalid documents {self.model}")
        q = generic_user_query(
            model,
            info.context.user,
            **filters
        )
        paginator = Paginator(
            q,
            size
        ).page(p + 1)
        docs = []
    
        return [
            DjangobaseDocumentNode(
              id=n.id,
              slug=n.slug,
              collection=self,
              data=n.to_data()
            )
            for
            n
            in
            paginator.object_list
        ]

    def resolve_document(self, info, slug):
        model = import_string(self.model)
        node = generic_user_get(
              model,
              slug,
              info.context.user,
        )
        
        return DjangobaseDocumentNode(
            data=node.to_data(),
            id=node.id,
            slug=node.slug,
            collection=self
        )


class DjangobaseFormField(graphene.ObjectType):
    name = graphene.Field(graphene.String)
    slug = graphene.Field(graphene.String)
    max_length = graphene.Field(graphene.Int)
    min_length = graphene.Field(graphene.Int)
    strip = graphene.Field(graphene.Boolean)
    max_digits = graphene.Field(graphene.Int)
    step_size = graphene.Field(graphene.Int)
    allow_unicode = graphene.Field(graphene.Boolean)
    empty_value = graphene.Field(graphene.String)
    type = graphene.Field(graphene.String)
    model = graphene.Field(graphene.String)
    help_text = graphene.Field(graphene.String)


class DjangobaseFormEntity(DjangoObjectType):
    class Meta:
        model = DjangoForm
        fields = ['name', 'slug', 'id']
    
    fields = graphene.List(
        'djangobase.schema.DjangobaseFormField'
    )

    def resolve_fields(self, info, slug):
        django_form = DjangoForm.objects.get(
            slug=slug
        )
        data = django_form.to_data()
        result = []
        for field in data.get('fields'):
            result.append(
                DjangobaseFormField(
                    slug=field.get('slug', ''),
                    name=field.get('name', ''),
                    help_text=field.get('help_text', ''),
                    type=field.get('type', ''),
                    model=field.get('model', ''),
                    max_length=field.get('max_length', 1),
                    min_length=field.get('min_length', 0)
                )
            )
        return result


class SubmitDjangoFormMutation(graphene.Mutation):
    class Arguments:
        form_id = graphene.String(required=True)
        data = graphene.JSONString(required=True)
        slug = graphene.String(required=False)

    status = graphene.Field(graphene.Int)

    def mutate(self, info, form_id, data, slug = None):
        django_form = DjangoForm.objects.get(
            slug=form_id
        )

        request = HttpRequest()
        request.user = info.context.user
        request.POST = QueryDict(
            **data
        ) 
        request.path = '/'

        result = django_form.submit_form(
            request,
            data,
            slug=slug
        )

        return SubmitDjangoFormMutation(
            status=201
        )


class DjangobaseQuery(graphene.ObjectType):
    collections = graphene.List(
        'djangobase.schema.DjangobaseCollectionNode'
    )
    collection = graphene.Field(
        'djangobase.schema.DjangobaseCollectionNode',
        slug=graphene.String(required=True)
    )

    def resolve_collections(self, info):
        return Collection.objects.all()
    
    def resolve_collection(self, info, slug):
        return Collection.objects.get(
            slug=slug
        )


class UpsertDjangobaseDocumentMutation(graphene.Mutation):
    class Arguments:
        slug = graphene.String(required=True)
        collection_id = graphene.String(required=True)
        data = graphene.JSONString(required=True)

    document = graphene.Field('djangobase.schema.DjangobaseDocumentNode')

    def mutate(self, info, slug, collection_id, data):
        if not info.context.user.is_authenticated:
            raise Exception("Not authenticated")

        collection = Collection.objects.get(
            slug=collection_id
        )

        model = import_string(collection.model)

        if not model:
            raise Exception(f"Invalid {collection.model}")

        node = None
        try:
            node = generic_user_get(
                model,
                info.context.user,
                slug=slug
            )
        except:
            pass
        
        if node:
            if hasattr(node, 'user'):
                if not node.user or node.user == info.context.user:
                    raise Exception("Cant edit another people's node")
            node.update_from_dict(data)
            node.save()
        else:
            node = model.upsert_from_data(info.context.user, data)
            if hasattr(node, 'user'):
                node.user = info.context.user
                node.save()
        return UpsertDjangobaseDocumentMutation(
            document=DjangobaseDocumentNode(
                data=node.to_data(),
                id=node.id,
                slug=node.slug,
                collection=collection
            )            
        )


class DjangobaseMutation(graphene.ObjectType):
    upsert_document = UpsertDjangobaseDocumentMutation.Field()


schema = graphene.Schema(query=DjangobaseQuery, mutation=DjangobaseMutation)

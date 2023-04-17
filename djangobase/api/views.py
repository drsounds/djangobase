from django.http import JsonResponse
from djangobase.models import Collection, CollectionGroup, Website


def api_get_collection(request, slug):
    collection = Collection.objects.get(
        slug=slug
    )

    return collection.to_data()


def api_get_collection_group(request, slug):
    collection_group = CollectionGroup.objects.get(
        slug=slug
    )

    return collection_group.to_data()


def api_get_collections(request):
    collections = Collection.objects.order_by('name').all()

    return JsonResponse(
       dict(objects=[
          collection.to_data()
          for
          collection
          in
          collections
       ])
    )


def api_get_collection_groups(request):
    collection_groups = CollectionGroup.objects.order_by('name').all()

    return JsonResponse(
       dict(objects=[
          collection_group.to_data()
          for
          collection_group
          in
          collection_groups
       ])
    )


def api_get_collections_for_site(request, slug):
    site = Website.objects.get(
        slug=slug
    )
    collections = Collection.objects.order_by('name').all()

    return JsonResponse(
       dict(objects=[
          collection.to_data()
          for
          collection
          in
          collections
       ])
    )


def api_get_collection_groups_for_site(request, slug):
    site = Website.objects.get(
        slug=slug
    )
    collection_groups = CollectionGroup.objects.order_by('name').all()

    return JsonResponse(
       dict(objects=[
          collection_group.to_data()
          for
          collection_group
          in
          collection_groups
       ])
    )


def api_get_sites(request):
    domain = request.GET.get('domain', None)

    filters = {
        
    }
    if domain:
          filters['domain__icontains'] = domain 
    sites = Website.objects.filter(
       **filters
    )
    return JsonResponse(
       dict(objects=[
         site.to_dict()
         for
         site
         in
         sites
       ])
    )



def api_get_site(request, slug=None):
    slug = request.GET.get('slug', slug)
    site = Website.objects.get(
       domain__icontains=slug
    )

    return JsonResponse(
       site.to_dict()
    )

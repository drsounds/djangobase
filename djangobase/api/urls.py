from django.urls import re_path
from djangobase.api.views import api_get_collection_group, api_get_collection_groups, api_get_collection_groups_for_site, api_get_sites, api_get_site, api_get_collection, api_get_collections, api_get_collections_for_site


urlpatterns = [
    re_path(r"^site/(?P<slug>\w+)", api_get_site, name='api_get_site'),
    re_path(r"^site/?P<slug>\w+/collections", api_get_collections_for_site, name='api_get_collections_for_site'),
    re_path(r"^site/?P<slug>\w+/collection_groups", api_get_collection_groups_for_site, name='api_get_collections_for_site'),
    re_path(r"^sites", api_get_sites, name='api_get_sites'),
    re_path(r"^collection/(?P<slug>\w+)", api_get_collection, name='api_get_collection'),
    re_path(r"^collection_group/(?P<slug>\w+)", api_get_collection_group, name='api_get_collection_group'),
    re_path(r"^collections", api_get_collections, name='api_get_collections'),
    re_path(r"^collection_groups", api_get_collection_groups, name='api_get_collection_groups')
]

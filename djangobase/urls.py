from django.urls import path, include
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from graphql_jwt.decorators import jwt_cookie
from django.views.decorators.csrf import csrf_exempt

import djangobase.api.urls


urlpatterns = [
    path(r"api/", include(djangobase.api.urls)),
    path("graphiql/", jwt_cookie(GraphQLView.as_view(graphiql=True))),
    path("graphql/", csrf_exempt(jwt_cookie(FileUploadGraphQLView.as_view()))),
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('film/', views.filmSearch, name='filmSearch'),
    path('film/<film_name>', views.filmSearch, name='filmSearch'),
    path('ajax_search_request', views.ajax_search_request, name='ajax_search_request'),
]

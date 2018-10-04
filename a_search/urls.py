from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('ajax_search_request', views.ajax_search_request, name='ajax_search_request'),
]

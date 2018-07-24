from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax_login', views.ajax_login, name='ajax_login'),
    path('ajax_reset', views.ajax_reset, name='ajax_reset'),
    path('ajax_register', views.ajax_register, name='ajax_register'),

]
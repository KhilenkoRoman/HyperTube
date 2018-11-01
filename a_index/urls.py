from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('activation', views.activation, name='activation'),
	path('reset_pwd', views.reset_pwd, name='reset_pwd'),
	path('ajax_login', views.ajax_login, name='ajax_login'),
	path('ajax_reset', views.ajax_reset, name='ajax_reset'),
	path('ajax_register', views.ajax_register, name='ajax_register'),
	path('ajax_new_pwd', views.ajax_new_pwd, name='ajax_new_pwd'),
	path('change_lang/<lang>', views.change_lang, name='change_lang'),
]

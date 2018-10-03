from django.urls import path

from . import views

urlpatterns = [
	path('', views.user_profile, name='user_profile'),
	path('profile/<user>', views.another_user_profile, name='another_user_profile'),
	path('social_activated/<provider>', views.social_activated, name='social_activated'),
	path('ajax_user_change_pwd', views.ajax_user_change_pwd, name='ajax_user_change_pwd'),
	path('ajax_user_change_info', views.ajax_user_change_info, name='ajax_user_change_info'),
	path('ajax_change_avatar', views.ajax_change_avatar, name='ajax_change_avatar'),
	path('logout',  views.logout_myself, name='logout_myself'),

]

from django.urls import path

from . import views

urlpatterns = [
    # path('', views.player, name='player'),
    path('ajax_comment', views.ajax_comment, name='ajax_comment'),
    path('ajax_torr_info', views.ajax_torr_info, name='ajax_torr_info'),
    path('ajax_del_comment', views.ajax_del_comment, name='ajax_del_comment'),
    path('test', views.test, name='test'),
    path('<film_id>', views.player, name='player'),
]

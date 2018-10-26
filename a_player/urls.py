from django.urls import path

from . import views

urlpatterns = [
    # path('', views.player, name='player'),
    path('ajax_comment', views.ajax_comment, name='ajax_comment'),
    path('test', views.test, name='test'),
    path('<film_id>', views.player, name='player'),

]

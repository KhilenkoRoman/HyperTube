from django.urls import path

from . import views

urlpatterns = [
	path('<get_login>', views.user_profile, name='user_profile'),
]
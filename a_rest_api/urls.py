from django.urls import path
from a_rest_api import views

urlpatterns = [
    path('users/', views.user_list),
    path('films/', views.film_list),
]

from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser')
	list_filter = ('is_staff', 'date_joined')
	filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)

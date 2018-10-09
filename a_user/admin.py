from django.contrib import admin
from a_user.models import CustomUserModel


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'date_joined')
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(CustomUserModel, UserAdmin)

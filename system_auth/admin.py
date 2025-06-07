from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    model = CustomUser

    list_display = ('email', 'username', 'id', 'first_name', 'last_name', 'phone', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'is_verified')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone', 'is_verified')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

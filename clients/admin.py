from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from clients.models import Client


class ClientAdmin(UserAdmin):

    model = Client
    list_display = ('email', 'username', 'first_name', 'last_name',
                    'gender', 'avatar', 'date_joined', 'last_login',
                    'is_admin', 'is_staff')
    list_filter = ('email', 'username')
    search_fields = ('email', 'username', 'gender')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('date_joined',)
    filter_horizontal = ()
    fieldsets = (
        ('Auth info', {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = fieldsets[:3]  # exclude 'Important dates'


admin.site.register(Client, ClientAdmin)

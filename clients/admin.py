from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from clients.models import Client, Match


class ClientAdmin(UserAdmin):
    model = Client
    list_display = ('id', 'email', 'username', 'first_name', 'last_name',
                    'gender', 'avatar', 'date_joined', 'last_login',
                    'is_admin', 'is_staff')
    readonly_fields = ('date_joined', 'last_login')

    list_filter = ('gender', 'is_staff', 'date_joined')
    search_fields = ('email', 'username')
    ordering = ('date_joined',)
    filter_horizontal = ()
    fieldsets = (
        ('Auth info', {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser')}),
        ('GeoInfo', {'fields': ('latitude', 'longitude')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
                        ('Auth info', {'fields': ('username', 'email', 'password1', 'password2')}),
                    ) + fieldsets[1:4]  # extend 'Auth info' and exclude 'Important dates'


admin.site.register(Client, ClientAdmin)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'recipient')


admin.site.register(Match, MatchAdmin)

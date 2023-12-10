from django.contrib import admin

from user.models import Team, User


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

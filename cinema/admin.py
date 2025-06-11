from django.contrib import admin

from cinema.models import Genre


@admin.register(Genre)
class MovieAdmin(admin.ModelAdmin):
    pass

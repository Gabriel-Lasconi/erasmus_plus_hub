from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'city', 'country', 'deadline')
    list_filter = ('type', 'country', 'deadline')
    search_fields = ('name', 'description', 'city', 'country')


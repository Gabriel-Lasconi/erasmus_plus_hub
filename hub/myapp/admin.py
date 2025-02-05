# myapp/admin.py
from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'city', 'country', 'deadline', 'created_at', 'approved')
    list_filter = ('type', 'country', 'deadline', 'approved')
    search_fields = ('name', 'description', 'city', 'country', 'submitted_by__username')
    ordering = ("-created_at",)



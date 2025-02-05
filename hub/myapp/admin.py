# myapp/admin.py
from .models import SuggestedProject
from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'city', 'country', 'deadline')
    list_filter = ('type', 'country', 'deadline')
    search_fields = ('name', 'description', 'city', 'country')

@admin.register(SuggestedProject)  # ✅ Correct way to register a model
class SuggestedProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "submitted_by", "approved", "created_at")
    list_filter = ("approved", "country")
    search_fields = ("title", "submitted_by")
    ordering = ("-created_at",)

    def approve_projects(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected projects approved successfully.")

    approve_projects.short_description = "Approve selected projects"


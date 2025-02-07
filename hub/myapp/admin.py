# myapp/admin.py
from .models import Project
from django.contrib import admin
from django.contrib.auth.models import User
from myapp.models import Profile, Badge

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'city', 'country', 'deadline', 'created_at', 'approved')
    list_filter = ('type', 'country', 'deadline', 'approved')
    search_fields = ('name', 'description', 'city', 'country', 'submitted_by__username')
    ordering = ("-created_at",)

# Extend UserAdmin to display Profile information
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"

# Extend UserAdmin to show Profile fields
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "get_country", "get_city", "get_phone")
    search_fields = ("username", "email", "profile__country", "profile__city")
    inlines = (ProfileInline,)

    def get_country(self, obj):
        return obj.profile.country if hasattr(obj, "profile") else "N/A"
    get_country.short_description = "Country"

    def get_city(self, obj):
        return obj.profile.city if hasattr(obj, "profile") else "N/A"
    get_city.short_description = "City"

    def get_phone(self, obj):
        return obj.profile.phone if hasattr(obj, "profile") else "N/A"
    get_phone.short_description = "Phone Number"

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Profile)
admin.site.register(Badge)



from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project, Profile


class CreateProjectForm(forms.ModelForm):
    """Form to create projects with automatic approval for staff users."""

    class Meta:
        model = Project
        fields = [
            "name", "description", "eligibility", "country", "city",
            "type", "deadline", "infopack_link", "application_link"
        ]

    def save(self, commit=True, user=None):
        project = super().save(commit=False)

        if user:
            project.submitted_by = user.username  # ✅ Save the user who submitted
            project.approved = user.is_staff  # ✅ Auto-approve if admin

        if commit:
            project.save()
        return project


class RegisterForm(UserCreationForm):
    """Custom user registration form with email validation."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Built-in fields

    def save(self, commit=True):
        """Override save to create user & profile."""
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)  # ✅ Ensure profile is created
        return user


class UserUpdateForm(forms.ModelForm):
    """Form to update User model details."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """Form to update additional profile information."""

    class Meta:
        model = Profile
        fields = [
            'profile_image', 'gender', 'date_of_birth', 'phone',
            'country', 'city', 'dietary_needs', 'bio'
        ]

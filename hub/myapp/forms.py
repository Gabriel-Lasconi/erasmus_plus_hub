from .models import Project
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "eligibility", "country", "city", "type", "deadline", "infopack_link", "application_link"]

    def save(self, commit=True, user=None):
        project = super().save(commit=False)
        if user and user.is_staff:  # ✅ If admin, auto-approve
            project.approved = True
        else:
            project.approved = False  # ✅ Normal users require approval
        if user:
            project.submitted_by = user.username  # ✅ Save the user who submitted
        if commit:
            project.save()
        return project

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Built-in fields

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'gender', 'date_of_birth', 'phone', 'country', 'city', 'dietary_needs', 'bio']

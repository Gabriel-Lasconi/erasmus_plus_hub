from django import forms
from .models import Project
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SuggestedProject

class ProjectForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
        label="Paste Message",
    )

    class Meta:
        model = Project
        fields = ["name", "description", "eligibility", "country", "city", "type", "deadline", "infopack_link", "application_link"]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Built-in fields


class SuggestedProjectForm(forms.ModelForm):
    class Meta:
        model = SuggestedProject
        fields = ['title', 'description']
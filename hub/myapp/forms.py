from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
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
            project.submitted_by = user.username
            project.approved = user.is_staff

        if commit:
            project.save()
        return project


class RegisterForm(UserCreationForm):
    """Custom user registration form with email validation."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        """Override save to create user & profile."""
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)
        return user


class UserUpdateForm(forms.ModelForm):
    """Form to update User model details."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """
    Form to update Profile details including:
      - phone (with country code picker)
      - date_of_birth (with HTML5 date input)
      - dietary preferences, etc.
    """

    # Explicitly add the date_of_birth so we can control its widget
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        ),
        required=False
    )

    phone = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(
            widgets=[
                forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose your country code'}),
                forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            ]
        ),
        label="Phone Number",
        help_text="Pick your country code, then enter your phone number."
    )

    class Meta:
        model = Profile
        fields = [
            'gender', 'city', 'country',
            'phone', 'date_of_birth',
            'bio', 'dietary_needs'
        ]
        widgets = {
            'gender': forms.Select(
                choices=Profile.GENDER_CHOICES,
                attrs={
                    'class': 'form-control',
                    'data-parsley-required': 'true',
                    'data-parsley-trigger': 'change'
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your city',
                    'data-parsley-required': 'true'
                }
            ),
            'country': CountrySelectWidget(
                attrs={
                    'class': 'form-control',
                    'data-parsley-required': 'true'
                }
            ),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Tell us something about yourself...',
                    'rows': 4
                }
            ),
            'dietary_needs': forms.Select(
                choices=Profile.DIETARY_CHOICES,
                attrs={
                    'class': 'form-control'
                }
            ),
        }

class ProfileImageForm(forms.ModelForm):
    """Separate form to handle just the profile image."""
    class Meta:
        model = Profile
        fields = ['profile_image']

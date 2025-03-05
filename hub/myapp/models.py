from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    """Stores details about organizations that post projects."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="organization_logos/", default="default_org.png")
    website = models.URLField(blank=True, null=True)

    def project_count(self):
        """Returns the number of projects associated with this organization."""
        return self.projects.count()

    def __str__(self):
        return self.name


class Project(models.Model):
    PROJECT_TYPES = [
        ('Youth Exchange', 'Youth Exchange'),
        ('Training Course', 'Training Course'),
        ('Conference', 'Conference'),
        ('Transnational Meeting', 'Transnational Meeting'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    eligibility = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=50, choices=PROJECT_TYPES)
    deadline = models.DateField(blank=True, null=True)
    infopack_link = models.URLField(blank=True, null=True)
    application_link = models.URLField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    submitted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name="projects")

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Certification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey('myapp.Project', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    issued_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Badge(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="badges/")
    users = models.ManyToManyField(User, related_name="badges")
    def __str__(self):
        return self.name

class Profile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    DIETARY_CHOICES = [
        ('none', 'No specific preference'),
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('halal', 'Halal'),
        ('kosher', 'Kosher'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)  # <- Make sure this exists
    dietary_needs = models.CharField(max_length=20, choices=DIETARY_CHOICES, default='none')
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_pics/", default="default.png")

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a profile when a user is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Ensure the profile is saved whenever the user is updated."""
    instance.profile.save()


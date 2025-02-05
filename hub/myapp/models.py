from django.contrib.auth.models import User
from django.db import models

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
    users = models.ManyToManyField(User, related_name="badges")  # ✅ Fix

    def __str__(self):
        return self.name


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_image = models.ImageField(upload_to="profile_pics/", default="default.jpg")
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    dietary_needs = models.TextField(blank=True, null=True)

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


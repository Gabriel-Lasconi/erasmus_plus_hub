from django.db import models
from django.contrib.auth.models import User

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

    approved = models.BooleanField(default=False)  # ✅ Ensure this exists
    submitted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

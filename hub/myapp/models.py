from django.db import models

class Project(models.Model):
    PROJECT_TYPES = [
        ('Youth Exchange', 'Youth Exchange'),
        ('Training Course', 'Training Course'),
        ('Conference', 'Conference'),
        ('Transnational Meeting', 'Transnational Meeting'),
    ]

    name = models.CharField(max_length=255)  # Project name
    description = models.TextField(blank=True, null=True)  # Project description
    eligibility = models.TextField(blank=True, null=True)  # Eligibility requirements
    country = models.CharField(max_length=100, blank=True, null=True)  # Country of the project
    city = models.CharField(max_length=100, blank=True, null=True)  # City of the project
    type = models.CharField(max_length=50, choices=PROJECT_TYPES)  # Dropdown for project types
    deadline = models.DateField(blank=True, null=True)  # Deadline of the project
    infopack_link = models.URLField(blank=True, null=True)  # Link to the infopack
    application_link = models.URLField(blank=True, null=True)  # Link to the application form

    def __str__(self):
        return self.name

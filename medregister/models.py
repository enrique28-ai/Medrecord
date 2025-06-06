from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from zoneinfo import available_timezones 
# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    age = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])

    def __str__(self):
        return self.name
    

class HealthRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_records')
    created_at = models.DateTimeField(auto_now_add=True)
    diagnostic = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    

    def __str__(self):
        return f"{self.patient.name} - {self.diagnostic}"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(
        max_length=32,
        default="America/Mexico_City",
        choices=sorted((tz, tz) for tz in available_timezones())
    )
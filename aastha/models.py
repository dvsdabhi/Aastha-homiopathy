from django.db import models
from django.utils import timezone

# Create your models here.

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    doctor = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('date', 'time')  # Prevent duplicate slots

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"

class TreatmentCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Treatment(models.Model):
    category = models.ForeignKey(TreatmentCategory, on_delete=models.CASCADE, related_name='treatments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='treatments/', blank=True, null=True)

    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
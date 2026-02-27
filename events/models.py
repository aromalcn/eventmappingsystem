from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    boundary_coordinates = models.JSONField(null=True, blank=True, help_text="List of [lat, lng] coordinates for the boundary polygon")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', default=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class EventSubsection(models.Model):
    """Represents a subsection/stage/area within an event"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='subsections')
    name = models.CharField(max_length=200, help_text="e.g., Main Stage, Food Court, VIP Area")
    description = models.TextField(blank=True, help_text="Optional details about this area")
    boundary_coordinates = models.JSONField(help_text="Polygon coordinates for this subsection")
    color = models.CharField(max_length=7, default='#ff7800', help_text="Hex color code for map display")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.event.title} - {self.name}"

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('ORGANIZER', 'Organizer'),
        ('USER', 'User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

class StageEvent(models.Model):
    """Represents a scheduled event occurring at a specific stage/subsection"""
    subsection = models.ForeignKey(EventSubsection, on_delete=models.CASCADE, related_name='scheduled_events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} @ {self.subsection.name}"


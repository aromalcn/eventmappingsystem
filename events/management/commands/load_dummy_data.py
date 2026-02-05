from django.core.management.base import BaseCommand
from events.models import Event, Category
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Loads dummy data for testing'

    def handle(self, *args, **kwargs):
        # Create Categories
        tech, _ = Category.objects.get_or_create(name='Technology')
        music, _ = Category.objects.get_or_create(name='Music')
        art, _ = Category.objects.get_or_create(name='Art')

        # Create Events
        events = [
            {
                'title': 'Tech Conference 2026',
                'description': 'A gathering of tech enthusiasts.',
                'date': timezone.now() + datetime.timedelta(days=10),
                'latitude': 37.7749,
                'longitude': -122.4194,
                'location_name': 'San Francisco, CA',
                'category': tech
            },
            {
                'title': 'Jazz Festival',
                'description': 'Smooth jazz all night long.',
                'date': timezone.now() + datetime.timedelta(days=20),
                'latitude': 29.9511,
                'longitude': -90.0715,
                'location_name': 'New Orleans, LA',
                'category': music
            },
            {
                'title': 'Modern Art Expo',
                'description': 'Showcasing contemporary artists.',
                'date': timezone.now() + datetime.timedelta(days=30),
                'latitude': 40.7128,
                'longitude': -74.0060,
                'location_name': 'New York, NY',
                'category': art
            },
             {
                'title': 'Bangalore Tech Summit',
                'description': 'Asia\'s largest tech summit.',
                'date': timezone.now() + datetime.timedelta(days=5),
                'latitude': 12.9716,
                'longitude': 77.5946,
                'location_name': 'Bangalore, India',
                'category': tech
            }
        ]

        for event_data in events:
            Event.objects.get_or_create(title=event_data['title'], defaults=event_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded dummy data'))

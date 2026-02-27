import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Category, Event, EventSubsection, StageEvent, UserProfile

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating data...')

        # 1. Categories
        categories = ['Music', 'Technology', 'Sports', 'Art', 'Food', 'Business', 'Health', 'Education']
        for name in categories:
            Category.objects.get_or_create(name=name)
        self.stdout.write(f'Categories: {Category.objects.count()}')

        # 2. Users & Profiles
        admin_user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True})
        admin_user.set_password('adminpass')
        admin_user.save()
        
        organizer_user, _ = User.objects.get_or_create(username='organizer1', defaults={'email': 'org1@example.com'})
        organizer_user.set_password('orgpass')
        organizer_user.save()
        UserProfile.objects.get_or_create(user=organizer_user, defaults={'role': 'ORGANIZER'})

        user1, _ = User.objects.get_or_create(username='user1', defaults={'email': 'user1@example.com'})
        user1.set_password('userpass')
        user1.save()
        UserProfile.objects.get_or_create(user=user1, defaults={'role': 'USER'})

        self.stdout.write(f'Users: {User.objects.count()}')

        # 3. Events
        tech_cat = Category.objects.get(name='Technology')
        music_cat = Category.objects.get(name='Music')

        # Event 1: Tech Conference
        event1, created = Event.objects.get_or_create(
            title='Future Tech Summit 2026',
            defaults={
                'description': 'The biggest tech conference of the year.',
                'date': timezone.now() + timedelta(days=30),
                'latitude': 37.7749,
                'longitude': -122.4194,
                'location_name': 'Moscone Center, SF',
                'category': tech_cat,
                'boundary_coordinates': [
                    [37.7750, -122.4200],
                    [37.7755, -122.4200],
                    [37.7755, -122.4190],
                    [37.7750, -122.4190],
                    [37.7750, -122.4200]
                ]
            }
        )
        
        # Event 2: Summer Music Festival
        event2, created = Event.objects.get_or_create(
            title='Summer Vibes Festival',
            defaults={
                'description': 'A weekend of great music and food.',
                'date': timezone.now() + timedelta(days=60),
                'latitude': 34.0522,
                'longitude': -118.2437,
                'location_name': 'LA Historic Park',
                'category': music_cat,
                'boundary_coordinates': [
                    [34.0520, -118.2440],
                    [34.0530, -118.2440],
                    [34.0530, -118.2430],
                    [34.0520, -118.2430],
                    [34.0520, -118.2440]
                ]
            }
        )
        self.stdout.write(f'Events: {Event.objects.count()}')

        # 4. Subsections
        # For Event 1
        main_hall, _ = EventSubsection.objects.get_or_create(
            event=event1,
            name='Main Hall',
            defaults={
                'description': 'Keynote speeches and big announcements.',
                'boundary_coordinates': [[37.7751, -122.4198], [37.7754, -122.4198], [37.7754, -122.4192], [37.7751, -122.4192]],
                'color': '#ff0000'
            }
        )
        
        workshop_area, _ = EventSubsection.objects.get_or_create(
            event=event1,
            name='Workshop Area',
            defaults={
                'description': 'Hands-on coding sessions.',
                'boundary_coordinates': [[37.7751, -122.4199], [37.7752, -122.4199], [37.7752, -122.4198], [37.7751, -122.4198]],
                'color': '#00ff00'
            }
        )

        # For Event 2
        main_stage, _ = EventSubsection.objects.get_or_create(
            event=event2,
            name='Main Stage',
            defaults={
                'description': 'The big acts perform here.',
                'boundary_coordinates': [[34.0522, -118.2438], [34.0528, -118.2438], [34.0528, -118.2432], [34.0522, -118.2432]],
                'color': '#0000ff'
            }
        )
        self.stdout.write(f'Subsections: {EventSubsection.objects.count()}')

        # 5. Stage Events
        # Main Hall Schedule
        StageEvent.objects.get_or_create(
            subsection=main_hall,
            title='Opening Keynote',
            defaults={
                'description': 'Welcome address by the CEO.',
                'start_time': event1.date,
                'end_time': event1.date + timedelta(hours=1)
            }
        )
        StageEvent.objects.get_or_create(
            subsection=main_hall,
            title='Future of AI',
            defaults={
                'description': 'Panel discussion on AI trends.',
                'start_time': event1.date + timedelta(hours=2),
                'end_time': event1.date + timedelta(hours=3)
            }
        )

        # Workshop Schedule
        StageEvent.objects.get_or_create(
            subsection=workshop_area,
            title='Python for Beginners',
            defaults={
                'description': 'Learn Python from scratch.',
                'start_time': event1.date + timedelta(hours=1),
                'end_time': event1.date + timedelta(hours=2.5)
            }
        )

        # Main Stage Schedule (Music)
        StageEvent.objects.get_or_create(
            subsection=main_stage,
            title='The Rockers',
            defaults={
                'description': 'Opening act.',
                'start_time': event2.date + timedelta(hours=18), # 6 PM
                'end_time': event2.date + timedelta(hours=19)
            }
        )
        StageEvent.objects.get_or_create(
            subsection=main_stage,
            title='Electro Beats',
            defaults={
                'description': 'Headliner DJ set.',
                'start_time': event2.date + timedelta(hours=20),
                'end_time': event2.date + timedelta(hours=22)
            }
        )
        self.stdout.write(f'StageEvents: {StageEvent.objects.count()}')

        # --- NEW DATA ---
        food_cat = Category.objects.get(name='Food')
        art_cat = Category.objects.get(name='Art')

        # Event 3: Global Food Expo
        event3, _ = Event.objects.get_or_create(
            title='Global Food Expo 2026',
            defaults={
                'description': 'Taste the world in one place.',
                'date': timezone.now() + timedelta(days=90),
                'latitude': 40.7128,
                'longitude': -74.0060,
                'location_name': 'Central Park, NY',
                'category': food_cat,
                'boundary_coordinates': [
                    [40.7130, -74.0070],
                    [40.7140, -74.0070],
                    [40.7140, -74.0050],
                    [40.7130, -74.0050],
                    [40.7130, -74.0070]
                ]
            }
        )

        # Event 4: Modern Art Showcase
        event4, _ = Event.objects.get_or_create(
            title='Modern Art Showcase',
            defaults={
                'description': 'Contemporary art from around the globe.',
                'date': timezone.now() + timedelta(days=120),
                'latitude': 51.5074,
                'longitude': -0.1278,
                'location_name': 'Tate Modern, London',
                'category': art_cat,
                'boundary_coordinates': [
                    [51.5070, -0.1280],
                    [51.5080, -0.1280],
                    [51.5080, -0.1270],
                    [51.5070, -0.1270],
                    [51.5070, -0.1280]
                ]
            }
        )
        self.stdout.write(f'Events (Updated): {Event.objects.count()}')

        # Subsections for Food Expo
        chefs_table, _ = EventSubsection.objects.get_or_create(
            event=event3,
            name="Chef's Table",
            defaults={
                'description': 'Live cooking demonstrations.',
                'boundary_coordinates': [[40.7132, -74.0065], [40.7135, -74.0065], [40.7135, -74.0060], [40.7132, -74.0060]],
                'color': '#ffa500'
            }
        )
        
        street_food_alley, _ = EventSubsection.objects.get_or_create(
            event=event3,
            name='Street Food Alley',
            defaults={
                'description': 'Best street food vendors.',
                'boundary_coordinates': [[40.7136, -74.0065], [40.7138, -74.0065], [40.7138, -74.0060], [40.7136, -74.0060]],
                'color': '#8b4513'
            }
        )

        # Subsections for Art Showcase
        main_gallery, _ = EventSubsection.objects.get_or_create(
            event=event4,
            name='Main Gallery',
            defaults={
                'description': 'Primary exhibition space.',
                'boundary_coordinates': [[51.5072, -0.1278], [51.5075, -0.1278], [51.5075, -0.1275], [51.5072, -0.1275]],
                'color': '#800080'
            }
        )
        self.stdout.write(f'Subsections (Updated): {EventSubsection.objects.count()}')

        # Schedules for Food Expo
        StageEvent.objects.get_or_create(
            subsection=chefs_table,
            title='Mastering Pasta',
            defaults={
                'description': 'Learn to make pasta from scratch.',
                'start_time': event3.date + timedelta(hours=11),
                'end_time': event3.date + timedelta(hours=12.5)
            }
        )
        StageEvent.objects.get_or_create(
            subsection=street_food_alley,
            title='Taco Tasting',
            defaults={
                'description': 'Try the best tacos in town.',
                'start_time': event3.date + timedelta(hours=13),
                'end_time': event3.date + timedelta(hours=15)
            }
        )

        # Schedules for Art Showcase
        StageEvent.objects.get_or_create(
            subsection=main_gallery,
            title='Curator Tour',
            defaults={
                'description': 'Guided tour with the lead curator.',
                'start_time': event4.date + timedelta(hours=10),
                'end_time': event4.date + timedelta(hours=11.5)
            }
        )
        self.stdout.write(f'StageEvents (Updated): {StageEvent.objects.count()}')

        # --- KERALA EVENTS ---
        sports_cat = Category.objects.get(name='Sports')
        
        # Event 5: Kochi Art Biennale
        event5, _ = Event.objects.get_or_create(
            title='Kochi Art Biennale',
            defaults={
                'description': 'International exhibition of contemporary art.',
                'date': timezone.now() + timedelta(days=150),
                'latitude': 9.9644,
                'longitude': 76.2238,
                'location_name': 'Fort Kochi, Kerala',
                'category': art_cat,
                'boundary_coordinates': [
                    [9.9640, 76.2230],
                    [9.9650, 76.2230],
                    [9.9650, 76.2245],
                    [9.9640, 76.2245],
                    [9.9640, 76.2230]
                ]
            }
        )

        # Event 6: Nehru Trophy Boat Race
        event6, _ = Event.objects.get_or_create(
            title='Nehru Trophy Boat Race',
            defaults={
                'description': 'Famous snake boat race on Punnamada Lake.',
                'date': timezone.now() + timedelta(days=200),
                'latitude': 9.5011,
                'longitude': 76.3424,
                'location_name': 'Alappuzha, Kerala',
                'category': sports_cat,
                'boundary_coordinates': [
                    [9.5000, 76.3420],
                    [9.5020, 76.3420],
                    [9.5020, 76.3430],
                    [9.5000, 76.3430],
                    [9.5000, 76.3420]
                ]
            }
        )
        self.stdout.write(f'Events (Kerala Added): {Event.objects.count()}')

        # Subsections for Kochi
        aspinwall, _ = EventSubsection.objects.get_or_create(
            event=event5,
            name='Aspinwall House',
            defaults={
                'description': 'Main venue for sea-facing installations.',
                'boundary_coordinates': [[9.9642, 76.2235], [9.9645, 76.2235], [9.9645, 76.2238], [9.9642, 76.2238]],
                'color': '#ff4500'
            }
        )

        # Subsections for Boat Race
        race_track, _ = EventSubsection.objects.get_or_create(
            event=event6,
            name='Race Track - Finish Point',
            defaults={
                'description': 'The exciting finish line area.',
                'boundary_coordinates': [[9.5010, 76.3422], [9.5012, 76.3422], [9.5012, 76.3425], [9.5010, 76.3425]],
                'color': '#008080'
            }
        )
        self.stdout.write(f'Subsections (Kerala Added): {EventSubsection.objects.count()}')

        # Schedules
        StageEvent.objects.get_or_create(
            subsection=aspinwall,
            title='Opening Ceremony',
            defaults={
                'description': 'Inauguration by cultural ministers.',
                'start_time': event5.date + timedelta(hours=9),
                'end_time': event5.date + timedelta(hours=11)
            }
        )
        StageEvent.objects.get_or_create(
            subsection=race_track,
            title='Snake Boat Finals',
            defaults={
                'description': 'The main race event.',
                'start_time': event6.date + timedelta(hours=14),
                'end_time': event6.date + timedelta(hours=17)
            }
        )
        self.stdout.write(f'StageEvents (Kerala Added): {StageEvent.objects.count()}')

        # Event 7: Thrissur Pooram
        cultural_cat, _ = Category.objects.get_or_create(name='Cultural')
        event7, _ = Event.objects.get_or_create(
            title='Thrissur Pooram',
            defaults={
                'description': 'The most spectacular festival in Kerala, famous for elephants and kudamattam.',
                'date': timezone.now() + timedelta(days=250),
                'latitude': 10.5244,
                'longitude': 76.2144,
                'location_name': 'Thekkinkadu Maidan, Thrissur',
                'category': cultural_cat,
                'boundary_coordinates': [
                    [10.5230, 76.2130],
                    [10.5260, 76.2130],
                    [10.5260, 76.2160],
                    [10.5230, 76.2160],
                    [10.5230, 76.2130]
                ]
            }
        )

        # Event 8: IFFK (International Film Festival of Kerala)
        film_cat, _ = Category.objects.get_or_create(name='Film')
        event8, _ = Event.objects.get_or_create(
            title='IFFK',
            defaults={
                'description': 'International Film Festival of Kerala.',
                'date': timezone.now() + timedelta(days=300),
                'latitude': 8.5068,
                'longitude': 76.9554,
                'location_name': 'Thiruvananthapuram, Kerala',
                'category': film_cat,
                'boundary_coordinates': [
                    [8.5060, 76.9550],
                    [8.5080, 76.9550],
                    [8.5080, 76.9560],
                    [8.5060, 76.9560],
                    [8.5060, 76.9550]
                ]
            }
        )
        self.stdout.write(f'Events (More Kerala): {Event.objects.count()}')

        # Subsections for Thrissur Pooram
        vadakkumnathan, _ = EventSubsection.objects.get_or_create(
            event=event7,
            name='Vadakkumnathan Temple Grounds',
            defaults={
                'description': 'The main temple premises.',
                'boundary_coordinates': [[10.5240, 76.2140], [10.5250, 76.2140], [10.5250, 76.2150], [10.5240, 76.2150]],
                'color': '#ffd700'
            }
        )

        # Subsections for IFFK
        tagore_theatre, _ = EventSubsection.objects.get_or_create(
            event=event8,
            name='Tagore Theatre',
            defaults={
                'description': 'Main venue for screenings.',
                'boundary_coordinates': [[8.5070, 76.9552], [8.5075, 76.9552], [8.5075, 76.9556], [8.5070, 76.9556]],
                'color': '#c0c0c0'
            }
        )
        self.stdout.write(f'Subsections (More Kerala): {EventSubsection.objects.count()}')

        # Schedules
        StageEvent.objects.get_or_create(
            subsection=vadakkumnathan,
            title='Ilanjithara Melam',
            defaults={
                'description': 'Traditional percussion performance.',
                'start_time': event7.date + timedelta(hours=10),
                'end_time': event7.date + timedelta(hours=14)
            }
        )
        StageEvent.objects.get_or_create(
            subsection=tagore_theatre,
            title='Opening Film Screening',
            defaults={
                'description': 'Premiere of the opening movie.',
                'start_time': event8.date + timedelta(hours=18),
                'end_time': event8.date + timedelta(hours=21)
            }
        )
        self.stdout.write(f'StageEvents (More Kerala): {StageEvent.objects.count()}')

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data.'))

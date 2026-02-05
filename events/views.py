from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, organizer_required, organizer_or_admin_required
from .forms import UserRegistrationForm, EventForm
from .forms import UserRegistrationForm, EventForm, UserEditForm, StageEventForm
from .models import Event, UserProfile, EventSubsection, StageEvent
from django.contrib.auth.models import User
from django.utils import timezone
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers using Haversine formula"""
    R = 6371  # Earth's radius in km
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

def landing_page(request):
    return render(request, 'events/landing.html')

def map_view(request):
    return render(request, 'events/map.html')

def event_list_api(request):
    # Get search query from request
    search_query = request.GET.get('search', '').strip()
    
    # Start with all events
    events = Event.objects.all()
    
    # Apply search filter if query exists
    if search_query:
        from django.db.models import Q
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location_name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    data = []
    for event in events:
        # Get subsections for this event
        subsections_data = []
        for subsection in event.subsections.all():
            subsections_data.append({
                'name': subsection.name,
                'description': subsection.description,
                'boundary_coordinates': subsection.boundary_coordinates,
                'name': subsection.name,
                'description': subsection.description,
                'boundary_coordinates': subsection.boundary_coordinates,
                'color': subsection.color,
                'id': subsection.id
            })
        
        data.append({
            'title': event.title,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d %H:%M'),
            'latitude': event.latitude,
            'longitude': event.longitude,
            'location_name': event.location_name,
            'category': event.category.name if event.category else 'Uncategorized',
            'boundary_coordinates': event.boundary_coordinates,
            'subsections': subsections_data,
            'id': event.id,
        })
    return JsonResponse(data, safe=False)

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='events.backends.EmailBackend')
            
            # Redirect based on role
            if hasattr(user, 'userprofile'):
                if user.userprofile.role == 'ADMIN':
                    return redirect('admin_dashboard')
                elif user.userprofile.role == 'ORGANIZER':
                    return redirect('organizer_dashboard')
                
            return redirect('user_dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'events/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirect based on role
            if hasattr(user, 'userprofile'):
                if user.userprofile.role == 'ADMIN':
                    return redirect('admin_dashboard')
                elif user.userprofile.role == 'ORGANIZER':
                    return redirect('organizer_dashboard')
            
            return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'events/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

@login_required
@organizer_or_admin_required
def add_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            
            # Handle subsections
            subsections_data = request.POST.get('subsections_data', '[]')
            try:
                import json
                from .models import EventSubsection
                subsections = json.loads(subsections_data)
                
                # Create EventSubsection objects
                for subsection in subsections:
                    EventSubsection.objects.create(
                        event=event,
                        name=subsection['name'],
                        description=subsection.get('description', ''),
                        boundary_coordinates=subsection['boundary_coordinates'],
                        color=subsection['color']
                    )
            except Exception as e:
                print(f"Error creating subsections: {e}")
            
            return redirect('map_home')
    else:
        # Pre-fill lat/long if provided in GET parameters
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})

@login_required
@organizer_or_admin_required
def edit_event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check permission
    if request.user.userprofile.role != 'ADMIN' and event.organizer != request.user:
        return redirect('organizer_dashboard')  # Or 403
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            # Ensure ownership doesn't change on edit unless admin?? 
            # Actually, standard is not to change owner.
            event.save()
            
            # Handle subsections - For simplicity, we'll clear existing and recreate
            # In a more complex app, we might want to track IDs to update instead of delete/create
            subsections_data = request.POST.get('subsections_data', '[]')
            try:
                import json
                from .models import EventSubsection
                subsections = json.loads(subsections_data)
                
                # Clear existing subsections
                event.subsections.all().delete()
                
                # Create new EventSubsection objects
                for subsection in subsections:
                    EventSubsection.objects.create(
                        event=event,
                        name=subsection['name'],
                        description=subsection.get('description', ''),
                        boundary_coordinates=subsection['boundary_coordinates'],
                        color=subsection['color']
                    )
            except Exception as e:
                print(f"Error updating subsections: {e}")
            
            if request.user.userprofile.role == 'ADMIN':
                return redirect('admin_dashboard')
            else:
                return redirect('organizer_dashboard')
    else:
        form = EventForm(instance=event)
    
    # Serialize subsections for the template
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    existing_subsections = list(event.subsections.values('name', 'description', 'boundary_coordinates', 'color'))
    existing_subsections_json = json.dumps(existing_subsections, cls=DjangoJSONEncoder)
    
    context = {
        'form': form,
        'is_edit': True,
        'event': event,
        'existing_subsections_json': existing_subsections_json
    }
    return render(request, 'events/add_event.html', context)

def nearby_events_api(request):
    """Find events within a specified radius of a location"""
    try:
        # Get parameters
        lat = float(request.GET.get('lat', 0))
        lon = float(request.GET.get('lon', 0))
        radius = float(request.GET.get('radius', 10))  # Default 10km
        
        # Get all events
        events = Event.objects.all()
        
        # Calculate distances and filter
        nearby_events = []
        for event in events:
            distance = haversine_distance(lat, lon, event.latitude, event.longitude)
            if distance <= radius:
                nearby_events.append({
                    'title': event.title,
                    'description': event.description,
                    'date': event.date.strftime('%Y-%m-%d %H:%M'),
                    'latitude': event.latitude,
                    'longitude': event.longitude,
                    'location_name': event.location_name,
                    'category': event.category.name if event.category else 'Uncategorized',
                    'boundary_coordinates': event.boundary_coordinates,
                    'id': event.id,
                    'id': event.id,
                    'distance': round(distance, 2),  # Distance in km
                    'subsections': [{
                        'name': s.name,
                        'description': s.description,
                        'boundary_coordinates': s.boundary_coordinates,
                        'color': s.color,
                        'id': s.id
                    } for s in event.subsections.all()]
                })
        
        # Sort by distance (closest first)
        nearby_events.sort(key=lambda x: x['distance'])
        
        return JsonResponse(nearby_events, safe=False)
    except (ValueError, TypeError) as e:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

@login_required
@admin_required
def admin_dashboard(request):
    from django.contrib.auth.models import User
    users = User.objects.all()
    events = Event.objects.all()
    return render(request, 'events/admin_dashboard.html', {
        'users': users, 
        'events': events,
        'total_users': users.count(),
        'total_events': events.count()
    })

@login_required
@organizer_required
def organizer_dashboard(request):
    # Only show events owned by the organizer
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'events/organizer_dashboard.html', {'events': events})

@login_required
def user_dashboard(request):
    return render(request, 'events/user_dashboard.html')

@login_required
@admin_required
def edit_user_view(request, user_id):
    user_to_edit = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserEditForm(instance=user_to_edit)
    return render(request, 'events/edit_user.html', {'form': form, 'user_to_edit': user_to_edit})

@login_required
@admin_required
def delete_user_view(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('admin_dashboard')
    return render(request, 'events/delete_user.html', {'user_to_delete': user_to_delete})

@login_required
@organizer_required
def manage_event_stages(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check ownership
    if request.user.userprofile.role != 'ADMIN' and event.organizer != request.user:
        return redirect('organizer_dashboard')

    subsections = event.subsections.all()
    return render(request, 'events/manage_event_stages.html', {'event': event, 'subsections': subsections})

@login_required
@organizer_required
def manage_stage_schedule(request, subsection_id):
    subsection = get_object_or_404(EventSubsection, id=subsection_id)
    
    # Check ownership via event
    if request.user.userprofile.role != 'ADMIN' and subsection.event.organizer != request.user:
        return redirect('organizer_dashboard')

    events = subsection.scheduled_events.all().order_by('start_time')
    return render(request, 'events/manage_stage_schedule.html', {'subsection': subsection, 'events': events})

@login_required
@organizer_required
def add_stage_event(request, subsection_id):
    subsection = get_object_or_404(EventSubsection, id=subsection_id)
    
    # Check ownership
    if request.user.userprofile.role != 'ADMIN' and subsection.event.organizer != request.user:
        return redirect('organizer_dashboard')

    if request.method == 'POST':
        form = StageEventForm(request.POST, subsection=subsection)
        if form.is_valid():
            stage_event = form.save(commit=False)
            stage_event.subsection = subsection
            stage_event.save()
            return redirect('manage_stage_schedule', subsection_id=subsection.id)
    else:
        form = StageEventForm(subsection=subsection)
    return render(request, 'events/add_stage_event.html', {'form': form, 'subsection': subsection})

def stage_details_api(request, subsection_id):
    subsection = get_object_or_404(EventSubsection, id=subsection_id)
    now = timezone.now()
    
    # Find live event (start <= now <= end)
    live_event = subsection.scheduled_events.filter(start_time__lte=now, end_time__gte=now).first()
    
    # Upcoming
    next_event = subsection.scheduled_events.filter(start_time__gt=now).order_by('start_time').first()
    upcoming_count = subsection.scheduled_events.filter(start_time__gt=now).count()
    
    data = {
        'id': subsection.id,
        'name': subsection.name,
        'live_event': {
            'title': live_event.title,
            'start': live_event.start_time.strftime('%H:%M'),
            'end': live_event.end_time.strftime('%H:%M')
        } if live_event else None,
        'next_event': {
            'title': next_event.title,
            'start': next_event.start_time.strftime('%H:%M')
        } if next_event else None,
        'upcoming_count': upcoming_count
    }
    return JsonResponse(data)

def stage_events_public_view(request, subsection_id):
    subsection = get_object_or_404(EventSubsection, id=subsection_id)
    now = timezone.now()
    
    upcoming_events = subsection.scheduled_events.filter(start_time__gte=now).order_by('start_time')
    past_events = subsection.scheduled_events.filter(end_time__lt=now).order_by('-start_time')
    live_event = subsection.scheduled_events.filter(start_time__lte=now, end_time__gte=now).first()
    
    return render(request, 'events/stage_events_public.html', {
        'subsection': subsection,
        'live_event': live_event,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'event': subsection.event
    })


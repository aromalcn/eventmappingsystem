from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    role = forms.ChoiceField(choices=[('USER', 'User'), ('ORGANIZER', 'Organizer')], widget=forms.RadioSelect, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Update user profile role
            if hasattr(user, 'userprofile'):
                user.userprofile.role = self.cleaned_data['role']
                user.userprofile.save()
        return user

from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location_name', 'latitude', 'longitude', 'category', 'boundary_coordinates']
        widgets = {
            'date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'boundary_coordinates': forms.HiddenInput(),
        }

class UserEditForm(forms.ModelForm):
    role = forms.ChoiceField(choices=[('ADMIN', 'Admin'), ('ORGANIZER', 'Organizer'), ('USER', 'User')], widget=forms.RadioSelect, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and hasattr(self.instance, 'userprofile'):
            self.fields['role'].initial = self.instance.userprofile.role

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if hasattr(user, 'userprofile'):
                user.userprofile.role = self.cleaned_data['role']
                user.userprofile.save()
        return user

from .models import StageEvent

class StageEventForm(forms.ModelForm):
    class Meta:
        model = StageEvent
        fields = ['title', 'description', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TextInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.TextInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")
            
            # We need the subsection to check for overlaps. 
            # Since the form doesn't have the subsection field (it's set in the view),
            # we might need to handle this validation slightly differently or assume 
            # the view handles passing the instance if updating, or we check in the view.
            # However, a robust way in ModelForm is to check in clean() but we need the subsection context.
            # Alternatively, control this in the view or pass subsection to form __init__.
            
            # For now, let's just validate times relative to each other here.
            # We will move the overlap validation to the model or view, 
            # OR better: pass the subsection to the form's __init__.
            pass
        return cleaned_data
        
    def __init__(self, *args, **kwargs):
        self.subsection = kwargs.pop('subsection', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")

            if self.subsection:
                from django.db.models import Q
                # Check for overlaps
                overlaps = self.subsection.scheduled_events.filter(
                    start_time__lt=end_time,
                    end_time__gt=start_time
                )
                
                if self.instance.pk:
                    overlaps = overlaps.exclude(pk=self.instance.pk)
                
                if overlaps.exists():
                    raise forms.ValidationError("This time slot overlaps with another event on this stage.")
        
        return cleaned_data

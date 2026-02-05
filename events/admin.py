from django.contrib import admin
from .models import Event, Category, EventSubsection

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location_name', 'category')
    search_fields = ('title', 'location_name')
    list_filter = ('category', 'date')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(EventSubsection)
class EventSubsectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'color', 'created_at')
    search_fields = ('name', 'event__title')
    list_filter = ('event', 'created_at')

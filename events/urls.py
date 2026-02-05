from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('map/', views.map_view, name='map_home'),
    path('api/events/', views.event_list_api, name='event_list_api'),
    path('api/events/nearby/', views.nearby_events_api, name='nearby_events_api'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-event/', views.add_event_view, name='add_event'),
    path('edit-event/<int:event_id>/', views.edit_event_view, name='edit_event'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/user/edit/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('dashboard/user/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('dashboard/organizer/', views.organizer_dashboard, name='organizer_dashboard'),
    path('organizer/event/<int:event_id>/stages/', views.manage_event_stages, name='manage_event_stages'),
    path('organizer/stage/<int:subsection_id>/schedule/', views.manage_stage_schedule, name='manage_stage_schedule'),
    path('organizer/stage/<int:subsection_id>/add-event/', views.add_stage_event, name='add_stage_event'),
    path('api/stage/<int:subsection_id>/details/', views.stage_details_api, name='stage_details_api'),
    path('stage/<int:subsection_id>/events/', views.stage_events_public_view, name='stage_events_public'),
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
]

from django.urls import path
from . import views

app_name = "site_cc"

urlpatterns = [
    path("calender/", views.calendar_view_new, name="calendar"),
    path("calenders/", views.calendar_view, name="calendars"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('next_week/<int:event_id>/', views.next_week, name='next_week'),
    path('next_day/<int:event_id>/', views.next_day, name='next_day'),
    path("event/new/", views.create_event, name="event_new"),
    path("event/edit/<int:event_id>/", views.calendar_view_new, name="edit_event"),  # Adicione esta linha
    path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    path("add_eventmember/<int:event_id>", views.add_eventmember, name="add_eventmember"),       
    path("event/<int:pk>/remove", views.event_member_delete, name="remove_event"),
    path("all-event-list/", views. all_events_list, name="all_events"),    
    path("running-event-list/", views.running_events_list, name="running_events"), 
    path('tempo/', views.tempo, name='tempo'),
    path('recomendacao/', views.recomendacao, name='recomendacao'),
    
]


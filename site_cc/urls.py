from django.urls import path
from . import views

app_name = "site_cc"

urlpatterns = [
    path("calender/", views.calendar_view_new, name="calendar"),
    path("calenders/", views.calendar_view, name="calendars"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('next_week/<int:event_id>/', views.next_week, name='next_week'),
    path('next_day/<int:event_id>/', views.next_day, name='next_day'),
    path("event/new/", views.create_or_edit_event, name="event_new"),
    path("event/new/plantio/", views.create_plantio_event, name="event_new_plantio"),  # Nova URL para eventos de Plantio
    path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    path("add_eventmember/<int:event_id>", views.add_eventmember, name="add_eventmember"),       
    path("event/<int:pk>/remove", views.event_member_delete, name="remove_event"),
    path("all-event-list/", views.all_events_list, name="all_events"),    
    path("running-event-list/", views.running_events_list, name="running_events"), 
    path('praga/', views.praga, name='praga'),
    path('recomendacao/', views.recomendacao, name='recomendacao'),
    path("event/plantio/<int:plantio_event_id>/create_colheita/", views.create_colheita_event, name="create_colheita_event"),

]

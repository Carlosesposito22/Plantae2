from datetime import datetime, timedelta
from django.db import models
from django.urls import reverse
from site_cc.models import EventAbstract
from accounts.models import User

class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_running_events(self, user):
        running_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now(),
        ).order_by("start_time")
        return running_events


class Event(EventAbstract):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    local = models.CharField(max_length=200, default='')
    type = models.CharField(max_length=50, default='') 
    cultura = models.CharField(max_length=50, default='') 
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_readable = models.CharField(max_length=200, null=True, blank=True) 
    
    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("site_cc:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("site_cc:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    @property
    def duration(self):
        """Calculate the duration of the event in days and hours."""
        if self.end_time and self.start_time:
            duration = self.end_time - self.start_time
            days = duration.days
            hours = (duration.seconds // 3600) % 24  # Get the remaining hours after full days
            return f"{days} dias, {hours} horas"
        return "0 dias, 0 horas"  # Return if times are not set

    def save(self, *args, **kwargs):
        # Atualiza o campo de duração legível antes de salvar
        if self.end_time and self.start_time:
            duration = self.end_time - self.start_time
            
            # Atualiza o campo de duração legível
            days = duration.days
            hours = (duration.seconds // 3600) % 24
            self.duration_readable = f"{days} dias, {hours} horas"
        
        super().save(*args, **kwargs)

from django.db import models

class ProblemaReportado(models.Model):
    plantio = models.CharField(max_length=100)
    descricao = models.TextField()
    data_reporte = models.DateTimeField(auto_now_add=True)
    resolvido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.plantio} - {self.descricao[:30]}"


from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from site_cc.models import Event
from site_cc.forms import EventForm


class DashboardView(View):
    login_url = "accounts:signin"
    template_name = "site_cc/dashboard.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.get_all_events(user=request.user)
        running_events = Event.objects.get_running_events(user=request.user)
        latest_events = Event.objects.filter(user=request.user).order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
        }
        return render(request, self.template_name, context)

class CalendarView(LoginRequiredMixin, View):
    login_url = "accounts:signin"

    def get(self, request, *args, **kwargs):
        event_id = request.GET.get('event_id')
        if request.method == "POST":
            event_id = request.POST.get('event_id')
            if event_id:
                event = get_object_or_404(Event, pk=event_id, user=request.user)
                form = EventForm(request.POST, instance=event)
            else:
                form = EventForm(request.POST)

            if form.is_valid():
                new_event = form.save(commit=False)
                new_event.user = request.user
                new_event.save()
                return redirect("site_cc:calendar")

        else:
            form = EventForm()
            if event_id:
                event = get_object_or_404(Event, id=event_id, user=request.user)
                form = EventForm(instance=event)

        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []

        for event in events:
            event_list.append({
                "id": event.id,
                "title": event.title,
                "type": event.type,
                "cultura": event.cultura,
                "local": event.local,
                "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "description": event.description,
                "duration_readable": event.duration_readable,
            })

        context = {
            "form": form,
            "events": event_list,
            "events_month": events_month
        }
        return render(request, "site_cc/calendar.html", context)

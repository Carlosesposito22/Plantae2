from django.contrib import admin
from django.urls import path, include
from .views import CalendarView, DashboardView


urlpatterns = [
    path("", CalendarView.as_view(), name="calendar"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("site_cc.urls")),
]

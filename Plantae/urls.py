from django.contrib import admin
from django.urls import path, include
from .views import CalendarView, DashboardView
from site_cc.views import homepage_view

urlpatterns = [
    path("", homepage_view, name="homepage"),  # Página inicial pública
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("site_cc/", include("site_cc.urls")),  # Inclui as URLs do site_cc com um prefixo
]

from django.urls import path

from accounts import views

app_name = "accounts"


urlpatterns = [
    path("signup/", views.sign_up_view, name="signup"),
    path("signin/", views.sign_in_view, name="signin"),
    path("signout/", views.signout, name="signout"),
]

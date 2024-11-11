from django.shortcuts import redirect
from django.contrib.auth import logout

def signout(request):
    logout(request)
    return redirect("site_cc:homepage")  # Redireciona para a homepage do site_cc

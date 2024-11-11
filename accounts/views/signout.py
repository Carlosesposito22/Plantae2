from django.shortcuts import redirect
from django.contrib.auth import logout




def signout(request):
    logout(request)
    return redirect("homepage")  
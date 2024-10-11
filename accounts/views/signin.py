
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from accounts.forms import SignInForm


def sign_in_view(request):
    template_name = "accounts/signin.html"
    
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("site_cc:calendar")
    else:
        form = SignInForm()

    context = {"form": form}
    return render(request,template_name, context)


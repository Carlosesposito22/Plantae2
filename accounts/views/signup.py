from django.shortcuts import render, redirect
from accounts.forms import SignUpForm

def sign_up_view(request):
    template_name = "accounts/signup.html"
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:signin")
    else:
        form = SignUpForm()

    context = {"form": form}
    return render(request, template_name, context)

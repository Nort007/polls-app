from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegistrationForm, LoginForm

# Create your views here.


@csrf_exempt
def signup_user(request):
    """Sign Up

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("index")

    else:
        form = RegistrationForm()

    return render(request, "signup.html", {"form": form})


@csrf_exempt
def login_user(request):
    """Login

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is None:
                return redirect("account:signup")
            login(request, user)
            # Редирект после успешной регистрации
            return redirect("index")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

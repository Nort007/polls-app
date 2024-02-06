from django.urls import path
from .views import signup_user, login_user

app_name = "account"
urlpatterns = [
    path("signup/", signup_user, name="signup"),
    path("login/", login_user, name="login"),
]

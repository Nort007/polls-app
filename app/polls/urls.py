from django.urls import path, include

from . import views

app_name = "polls"

urlpatterns = [
    path("poll/<int:poll_id>/", views.poll, name="poll"),
    path("poll/<int:poll_id>/results/", views.poll_result, name="poll_result"),
]

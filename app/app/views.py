from django.shortcuts import render

from polls.models import Poll


def index(request):
    polls = Poll.objects.all()
    return render(request, "index.html", {"polls": polls})

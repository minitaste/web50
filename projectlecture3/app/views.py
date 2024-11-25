from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "app/index.html")

def the_sun(request):
    return HttpResponse("Hello Sun")

def greet(request, name):
    return render(request, "app/greet.html", {
        "name": name.title()
    })
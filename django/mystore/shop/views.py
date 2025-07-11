from django.shortcuts import render
from django.http import HttpResponse
def home(request):
    return HttpResponse("<h2>Hello World! namaste all of you</h2>")
# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse

def users(request):
    return HttpResponse("Hello world!")

def normal(request):
    return HttpResponse("Normal Page")

def caching(request):
    return HttpResponse("Caching Page")

def sharding(request):
    return HttpResponse("Sharding Page")
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import  HttpResponse
# Create your views here.

def hello(requst):
    return HttpResponse("Hello World")

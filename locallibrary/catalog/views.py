from django.shortcuts import render
from django.http import HttpResponse



def index(request):
   return HttpResponse('Welcome at the library.')
# Create your views here.

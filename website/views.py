# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader


def index(request):
    context = {}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def login(request):
    context = {}
    context['navbar_style'] = 'none'
    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


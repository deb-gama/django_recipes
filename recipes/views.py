from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('HOME')


def contact(request):
    return HttpResponse('CONTATO')


def about(request):
    return HttpResponse('SOBRE')

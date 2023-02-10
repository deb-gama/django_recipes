from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse

from .forms import RegisterForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    title = 'Auhors | Register'
    form = RegisterForm(register_form_data)

    return render(
        request,
        'authors/pages/register_view.html',
        {
            'form': form,
            'title': title
        }
    )

def register_create(request):
    if  not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    return redirect('authors:register')



from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse

from .forms import RegisterForm


def register_view(request):
    # register_form_data = request.session.get('register_form_data', None)
    title = 'Auhors | Register'
    if request.POST:
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm()

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
    request.session['register_fomr_data'] = POST
    form = RegisterForm(POST)

    return redirect(request,'authors:register')



from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages

from .forms import RegisterForm


def register_view(request):
    """
    This view is responsible for rendering an empty form when in GET mode and
    receiving the register_form_data in the register redirection  create view.
    """
    title = 'Auhors | Register'
    register_form_data = request.session.get('register_form_data', None)
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
    """
    This view will log the new user or throw an error if something is wrong.
    Redirect to register_view to disallow resubmit of the form.
    """
    if  not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'User successfully created. Please log in')

        del(request.session['register_form_data'])

    return redirect('authors:register')



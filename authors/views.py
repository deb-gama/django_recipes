from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm

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
        user = form.save(commit=False)
        #criptografando a senha antes de salvar na database
        user.set_password(user.password)
        user.save()
        messages.success(request, 'User successfully created. Please log in')

        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    title = 'Auhors | Login'
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'title': title,
        'form': form,
        'form_action': reverse('authors:login_create')
        }
    )


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            messages.success(request, 'Your are logged in')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(login_url)

@login_required(login_url='authors:logout', redirect_field_name='next')
def logout_view(request):
    logout(request)
    return redirect(reverse('authors:login'))

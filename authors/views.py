from django.shortcuts import render
from django.http import Http404

from .forms import RegisterForm


def register_view(request):
    request.session['number'] = request.session.get('number') or 1
    # somando aqui para desconsiderar o NONE que recebemos no primeiro acesso
    request.session['number'] += 1
    form = RegisterForm()
    title = 'Auhors | Register'
    return render(request, 'authors/pages/register_view.html', {'form': form, 'title':title})

def register_create(request):
    if  not request.POST:
        raise Http404()
    form = RegisterForm(request.POST)

    title = 'Auhors | Register'
    return render(request, 'authors/pages/register_view.html', {'form': form, 'title':title})



from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe

from authors.forms import LoginForm, RegisterForm, AuthorRecipeForm, AuthorCreateRecipeForm

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
    """
    This view makes the authentication logic and redirect de user for login_view with
    appropriate messages of success or failed.
    """
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    # login_url = reverse('authors:login')

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

    return redirect(reverse('authors:dashboard'))

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    """
    View wich contains the logout logical and messages. Redirect the user back for login view.
    """
    if not request.POST:
        return redirect(reverse('authors:login'))

    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_view(request):
    """
    This view lists the author´s recipes.
    """
    title = 'Authors | Dashboard'
    recipes = Recipe.objects.filter(
        is_published=False,
        author = request.user,
    )

    return render(request, 'authors/pages/dashboard.html', {
      'title': title,
      'recipes': recipes,
      }
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, recipe_id):
    """
    This view makes it possible to edit recipes
    """
    title = 'Authors | Dashboard Edit Recipe'
    recipe = Recipe.objects.filter(
        is_published=False,
        author = request.user,
        pk = recipe_id,
    ).first()

    if not recipe:
        raise Http404()

    form =AuthorRecipeForm(request.POST or None,files=request.FILES or None, instance=recipe)

    if form.is_valid():
        # salvando os dados na variável antes de salvar na base de dados
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_step_is_html = False
        recipe.is_published = False

        # salvando na base de dados após verifcações feitas acima
        recipe.save()
        messages.success(request, 'Your recipe was saved!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe_id,)))

    return render(request, 'authors/pages/dashboard_recipe.html', {
      'title': title,
      'recipe': recipe,
      'form': form,
      }
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):
    """
    This view makes it possible to create new recipes
    """
    title = 'Authors | Dashboard Create Recipe'
    recipe = Recipe()

    form =AuthorCreateRecipeForm(request.POST or None,files=request.FILES or None, instance=recipe)

    if form.is_valid():
        # salvando os dados na variável antes de salvar na base de dados
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_step_is_html = False
        recipe.is_published = False

        # salvando na base de dados após verifcações feitas acima
        recipe.save()
        messages.success(request, 'Your recipe was created!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))
        # return redirect(reverse('authors:dashboard_recipe_create'))

    return render(request, 'authors/pages/dashboard_recipe_create.html', {
      'title': title,
      'form': form,
      }
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    """
    This view makes it possible to delete recipes
    """
    if  not request.POST:
        raise Http404()

    POST = request.POST
    recipe_id = POST.get('id')

    recipe = Recipe.objects.filter(
        is_published=False,
        author = request.user,
        pk = recipe_id,
    ).first()

    if not recipe:
        raise Http404()

    recipe.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('authors:dashboard')









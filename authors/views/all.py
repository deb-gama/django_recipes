from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import (
    AuthorCreateRecipeForm,
    AuthorRecipeForm,
    LoginForm,
    RegisterForm,
)
from recipes.models import Recipe


def register_view(request):
    """
    This view is responsible for rendering an empty form when in GET mode and
    receiving the register_form_data in the register redirection  create view.
    """
    title = "Authors | Register"
    register_form_data = request.session.get("register_form_data", None)
    form = RegisterForm(register_form_data)

    return render(
        request, "authors/pages/register_view.html", {"form": form, "title": title}
    )


def register_create(request):
    """
    This view will log the new user or throw an error if something is wrong.
    Redirect to register_view to disallow resubmit of the form.
    """
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session["register_form_data"] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        # encrypting the password before saving to the database
        user.set_password(user.password)
        user.save()
        messages.success(request, "User successfully created. Please log in")

        del request.session["register_form_data"]
        return redirect(reverse("authors:login"))

    return redirect("authors:register")


def login_view(request):
    title = "Authors | Login"
    form = LoginForm()
    return render(
        request,
        "authors/pages/login.html",
        {
            "title": title,
            "form": form,
            "is_login_page": True,
            "form_action": reverse("authors:login_create"),
        },
    )


def login_create(request):
    """
    This view makes the authentication logic and redirect de user for login_view with
    appropriate messages of success or failed.
    """
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get("username", ""),
            password=form.cleaned_data.get("password", ""),
        )
        if authenticated_user is not None:
            messages.success(request, "You are logged in")
            login(request, authenticated_user)
        else:
            messages.error(request, "Invalid credentials")
    else:
        messages.error(request, "Invalid username or password")

    return redirect(reverse("authors:dashboard"))


@login_required(login_url="authors:login", redirect_field_name="next")
def logout_view(request):
    """
    View wich contains the logout logical and messages. Redirect the user back for login view.
    """
    if not request.POST:
        return redirect(reverse("authors:login"))

    messages.success(request, "Logged out successfully")
    logout(request)
    return redirect(reverse("authors:login"))


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_view(request):
    """
    This view lists the author´s recipes.
    """
    title = "Authors | Dashboard"
    recipes = Recipe.objects.filter(
        author=request.user,
    ).order_by("is_published")

    return render(
        request,
        "authors/pages/dashboard.html",
        {
            "title": title,
            "recipes": recipes,
            "is_dashboard_page": True,
        },
    )

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm, AuthorRecipeForm
from django.http import Http404, HttpResponseNotAllowed, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe

# Create your views here.
def register_view(request):
    register_form_data = request.session.get("register_form_data", None)
    form = RegisterForm(register_form_data)
    return render(
        request,
        "register.html",
        {"form": form, "form_action": reverse("authors:register_create")},
    )


def register_create(request):
    if not request.POST:
        raise Http404

    request.session["register_form_data"] = request.POST
    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, "Your user is created, please log in.")
        del request.session["register_form_data"]
        return redirect(reverse("authors:login"))

    return redirect("authors:register")


def login_view(request):
    return render(
        request,
        "login.html",
        {"form": LoginForm(), "form_action": reverse("authors:login_create")},
    )


def login_create(request):
    if not request.POST:
        raise HttpResponseNotAllowed()

    form = LoginForm(request.POST)
    login_url = reverse("authors:login")

    if not form.is_valid():
        raise HttpResponseBadRequest("Error to validate form data")

    authenticated_user = authenticate(
        username=form.cleaned_data.get("username"),
        password=form.cleaned_data.get("password"),
    )

    if not authenticated_user:
        messages.error(request, "Invalid credentials")
        return redirect(login_url)

    messages.success(request, "Your are logged in")
    login(request, authenticated_user)
    return redirect("authors:dashboard")


@login_required(login_url="authors:login", redirect_field_name="next")
def logout_view(request):

    if not request.POST:
        messages.error(request, "Invalid logout request")
        return redirect("authors:login")

    if request.POST.get("username") != request.user.username:
        messages.error(request, "Invalid logout user")
        return redirect("authors:login")

    messages.success(request, "Logged out successfully")
    logout(request)
    return redirect("authors:login")


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard(request):
    recipes = Recipe.objects.filter(is_published=False, author=request.user)
    return render(request, "dashboard.html", context={"recipes": recipes})


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.get(
        is_published=False,
        author=request.user,
        pk=id,
    )

    return render(request, "dashboard_recipe.html", context={
        "recipe": recipe,
        "form": AuthorRecipeForm(
            data=request.POST or None,
            instance=recipe
        )
    })

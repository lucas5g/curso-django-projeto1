from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Recipe


# Create your views here.
def home(request):
    # Sem 404 aqui: o template já trata lista vazia com {% empty %}
    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by("-id")
    return render(request, "home.html", context={"recipes": recipes})


def category(request, category_id):
    # recipes = get_list_or_404(Recipe.objects.filter(
    #     category__id=category_id,
    #     is_published=True,
    # ).order_by('-id'))
    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published=True,
    ).order_by("-id")

    if not recipes:
        raise Http404()

    return render(
        request,
        "category.html",
        context={"recipes": recipes, "title": f"{recipes.first().category.name}"},
    )


def recipe(request, id):
    # Recipe.objects.filter(
    #     pk=id,
    #     is_published=True,
    # ).order_by('-id').first()
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(
        request, "recipe.html", context={"recipe": recipe, "is_detail_page": True}
    )

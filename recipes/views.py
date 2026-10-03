from django.shortcuts import get_object_or_404, render

from .models import Recipe


# Create your views here.
def home(request):
    recipes = Recipe.objects.all().order_by('-id')
    return render(request, 'home.html', context={
        'recipes': recipes
    })


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id
    ).order_by('-id')
    return render(request, 'home.html', context={
        'recipes': recipes
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    return render(request, 'recipe.html', context={
        'recipe': recipe,
        'is_detail_page': True
    })

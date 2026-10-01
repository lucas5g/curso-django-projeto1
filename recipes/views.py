from django.shortcuts import render
from django.http.response import HttpResponse
from utils.recipes.factory import make_recipe
# Create your views here.
def home(request):
    return render(request, 'home.html', context={
        'recipes': [make_recipe() for _ in range(10)]
    })


def recipe(request, id):
    return render(request, 'recipe.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True
    })

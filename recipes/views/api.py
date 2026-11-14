from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.get_published().values(
        *RecipeSerializer.Meta.fields
    )[:10]
    serializer = RecipeSerializer(instance=recipes, many=True)
    return Response(serializer.data)

@api_view()
def recipe_api_detail(request, pk):    
    recipe = get_object_or_404(
        Recipe.objects.get_published().values(*RecipeSerializer.Meta.fields), pk=pk
    )
    
    serializer = RecipeSerializer(instance=recipe)
    return Response(serializer.data)

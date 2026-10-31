from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name="category"),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/<int:pk>', views.RecipeDetail.as_view(), name='recipe'),
    path('api/recipes', views.RecipeListViewHomeApi.as_view(), name="api_recipes"),
    path('api/recipes/<int:pk>', views.RecipeDetailApi.as_view(), name="api_recipe_detail")

]

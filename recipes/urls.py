from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name="category"),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/<int:pk>', views.RecipeDetail.as_view(), name='recipe'),
    # path('api/recipes', views.RecipeListViewHomeApi.as_view(), name="api_recipes"),
    # path('api/recipes/<int:pk>', views.RecipeDetailApi.as_view(), name="api_recipe_detail"),
    path('recipes/theory', views.theory, name='theory'),
    path('recipes/tags/<slug:slug>', views.RecipeListViewTag.as_view(), name='tag'),
    path('api/recipes', views.api.recipe_api_list, name='recipes_api_v2' ),
    path('api/recipes/<int:pk>', views.api.recipe_api_detail, name='recipes_api_v2_detail' ),
    path('api/recipes/tag/<int:pk>', views.tag_api_detail, name='recipes_api_v2_tag')

]

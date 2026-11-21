from django.urls import path, include
from recipes import views
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'recipes'

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.trailing_slash = '/?'
recipe_api_v2_router.register(
    'api/recipes', views.api.RecipeAPIv2ViewSet,
    basename='recipe-api',    
)


urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name="category"),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/<int:pk>', views.RecipeDetail.as_view(), name='recipe'),
    # path('api/recipes', views.RecipeListViewHomeApi.as_view(), name="api_recipes"),
    # path('api/recipes/<int:pk>', views.RecipeDetailApi.as_view(), name="api_recipe_detail"),
    path('recipes/theory', views.theory, name='theory'),
    path('recipes/tags/<slug:slug>', views.RecipeListViewTag.as_view(), name='tag'),
    path('', include(recipe_api_v2_router.urls)),
    # path('api/recipes', views.api.RecipeAPIv2ViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create'
    # }), name='recipes_api_v2' ),
    # path('api/recipes/<int:pk>', views.api.RecipeAPIv2ViewSet.as_view({
    #     'get': 'retrieve',
    #     'patch': 'partial_update',
    #     'delete': 'destroy'
    # }), name='recipes_api_v2_detail' ),
    path('api/recipes/tag/<int:pk>', views.tag_api_detail, name='recipes_api_v2_tag'),
    path('recipes/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('recipes/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('recipes/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer
from django.shortcuts import get_object_or_404
from tags.models import Tag
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 5


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination

    def get_queryset(self):
        qs = super().get_queryset()

        print('Parâmetros ', self.kwargs)
        print('Query strings ',  self.request.query_params)

        category_id = self.request.query_params.get('category_id', None)

        if category_id and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

# class RecipeAPIv2List(ListCreateAPIView):
#     queryset = Recipe.objects.get_published()
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeAPIv2Pagination


# class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
#     queryset = Recipe.objects.get_published()
#     serializer_class = RecipeSerializer

#     def patch(self, request, *args, **kwargs):
#         recipe = self.get_object()

#         serializer = self.get_serializer(
#             instance=recipe, data=request.data, partial=True
#         )

#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data)

# class RecipeAPIv2List(ListCreateAPIView):
# queryset = Recipe.objects.get_published()
# serializer_class = RecipeSerializer
# pagination_class = RecipeAPIv2Pagination
# class RecipeAPIv2List(APIView):
#     def get(self, request):
#         recipes = Recipe.objects.get_published()[:10]
#         serializer = RecipeSerializer(
#             instance=recipes, many=True, context={"request": request}
#         )
#         return Response(serializer.data)

#     def post(self, request):
#         serializer= RecipeSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(
#             # author_id=1, category_id=1, tags=[1, 2]
#         )
#         return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


# class RecipeAPIv2Detail(APIView):
#     def get_recipe(self, pk):
#         recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)

#     def get(self, request, pk):
#         recipe = self.get_recipe(pk)
#         serializer = RecipeSerializer(
#             instance=recipe, many=False, context={"request": request}
#         )
#         return Response(serializer.data)

#     def patch(self, requeest, pk):
#         recipe = self.get_recipe(pk)
#         serializer = RecipeSerializer(
#             instance=recipe, data=request.data, partial=True, context={"request": request}
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, pk):

#         recipe = self.get_recipe(pk)
#         recipe.delete()
#         return Response({
#             'message': 'Recipe was deleted successfully'
#         }, status=status.HTTP_204_NO_CONTENT)


# @api_view(['get', 'patch', 'delete'])
# def recipe_api_detail(request, pk):

#     if request.method == "PATCH":


#     if request.method == 'DELETE':
#         recipe.delete()
#         return Response({
#             'message': 'Recipe was deleted successfully'
#         }, status=status.HTTP_204_NO_CONTENT)

#     serializer = RecipeSerializer(
#         instance=recipe, many=False, context={"request": request}
#     )

#     return Response(serializer.data)


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.filter(), pk=pk)

    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)

import os

from django.contrib import messages
from django.db.models import Q
from django.db.models.aggregates import Count, Max, Min, Sum

from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from utils.pagination import make_pagination, make_pagination_range
from tags.models import Tag
from .models import Recipe
from django.utils import translation
from django.utils.translation import gettext as _

PER_PAGE = int(os.environ.get("PER_PAGE", 6))


def theory(request, *args, **kwargs):
    # recipes = Recipe.objects.all()
    # try:
    #     recipes = recipes.get(pk=2789)
    # except ObjectDoesNotExist:
    #     recipes = None
    # recipes = recipes.filter(id=1).order_by('-id').last()
    # recipes = recipes.filter(title__icontains='lasanha').last()
    #
    #     recipes = Recipe.objects.filter(
    #         Q(title__icontains="lasanha", id__gt=2) | Q(id__gt=1000)
    #     )[:10]
    # recipes = Recipe.objects.filter(
    #     id=F('author__id')
    # ).select_related('author')

    # recipes = Recipe.objects.values("id", "title")[:10]
    # recipes = Recipe.objects.only("id", "title")[:10]
    # recipes = Recipe.objects.defer('is_published')[:10]
    # recipes = Recipe.objects.values('id', 'title').filter(author_id__gt=1)
    # recipes = Recipe.objects.values('id', 'title')[:5]
    # recipes = Recipe.objects.all()[:5]
    recipes = Recipe.objects.get_published()[:5]
    number_of_recipes = recipes.aggregate(Count("id"))

    context = {"recipes": recipes, "number_of_recipes": number_of_recipes["id__count"]}

    return render(
        request,
        "theory.html",
        context,
    )


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = "recipes"
    paginate_by = PER_PAGE
    ordering = ["-id"]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True)
        qs = qs.select_related("author", "category")
        qs = qs.prefetch_related("tags", "author__profile")

        return qs

    def get_context_data(self):
        ctx = super().get_context_data()
        page_obj, pagination_range = make_pagination(
            self.request, self.get_queryset(), PER_PAGE
        )

        html_language = translation.get_language()

        ctx.update(
            {
                "pagination_range": pagination_range,
                "recipes": page_obj,
                "html_language": html_language,
            },
        )

        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = "home.html"


class RecipeListViewCategory(RecipeListViewBase):
    template_name = "category.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            category__id=self.kwargs.get("category_id"),
            is_published=True,
        )

        if not qs:
            raise Http404()

        return qs


class RecipeListViewSearch(RecipeListViewBase):
    template_name = "search.html"

    def get_queryset(self):
        search_term = self.request.GET.get("q", "").strip()

        if not search_term:
            raise Http404()

        qs = super().get_queryset()

        return qs.filter(
            Q(title__icontains=search_term) | Q(description__icontains=search_term)
        ).order_by("-id")

    def get_context_data(self):
        ctx = super().get_context_data()
        search_term = self.request.GET.get("q", "")

        ctx.update(
            {
                "search_term": search_term,
                "page_title": f'Search for "{search_term}"',
            }
        )
        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipe.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("tags")
        return qs.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx.update({"is_detail_page": True})
        return ctx


class RecipeListViewHomeApi(RecipeListViewBase):
    # template_name = 'home.html'
    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()["recipes"]
        recipes_list = recipes.object_list.values()
        return JsonResponse(list(recipes_list), safe=False)


class RecipeDetailApi(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()["recipe"]
        recipe_dict = model_to_dict(recipe)

        recipe_dict["created_at"] = str(recipe.created_at)
        recipe_dict["updated_at"] = str(recipe.updated_at)

        if recipe_dict.get("cover"):
            recipe_dict["cover"] = self.request.build_absolute_uri(recipe.cover.url)

        return JsonResponse(recipe_dict, safe=False)


class RecipeListViewTag(RecipeListViewBase):
    template_name = "tag.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get("slug"))

        # qs = qs.select_related('author')
        # qs = qs.prefetch_related('tag')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(slug=kwargs.get("slug", "")).first()

        if not page_title:
            page_title = "No recipes found"

        page_title = f"{page_title} - Tag |"
        ctx.update(
            {
                "page_title": page_title,
            }
        )

        return ctx


# Create your views here.
def home(request):
    # Sem 404 aqui: o template já trata lista vazia com {% empty %}
    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by("-id")

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request,
        "home.html",
        context={
            "recipes": page_obj,
            "pagination_range": pagination_range,
        },
    )


def category(request, category_id):

    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published=True,
    ).order_by("-id")

    if not recipes:
        raise Http404()

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request,
        "category.html",
        context={
            "recipes": page_obj,
            "title": f"{recipes.first().category.name}",
            "pagination_range": pagination_range,
        },
    )


def recipe(request, id):
    recipe = Recipe.objects.get(
        pk=id,
        is_published=True,
    )
    return render(
        request, "recipe.html", context={"recipe": recipe, "is_detail_page": True}
    )


def search(request):

    search_term = request.GET.get("q", "").strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(title__icontains=search_term) | Q(description__icontains=search_term),
        is_published=True,
    ).order_by("-id")

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request,
        "search.html",
        context={
            "page_title": f'Search for "{search_term}"',
            "search_term": search_term,
            "recipes": page_obj,
            "pagination_range": pagination_range,
            "additional_url_query": f"&q={search_term}",
        },
    )

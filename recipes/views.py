import os
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from .models import Recipe
from utils.pagination import make_pagination, make_pagination_range
from django.contrib import messages
from django.views.generic import ListView, DetailView

PER_PAGE = int(os.environ.get("PER_PAGE", 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = "recipes"
    paginate_by = PER_PAGE
    ordering = ["-id"]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True)

        return qs

    def get_context_data(self):
        ctx = super().get_context_data()
        page_obj = ctx['page_obj']

        pagination_range = make_pagination_range(
            page_obj.paginator.page_range, 5,
            page_obj.number
        )

        ctx.update(
            {
                "pagination_range": pagination_range,
                "recipes": page_obj
            },
        )

        return ctx

class RecipeListViewHome(RecipeListViewBase):
    template_name = 'home.html'

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'category.html'

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
    template_name = 'search.html'

    def get_queryset(self):
        search_term = self.request.GET.get("q", "").strip()
        qs = super().get_queryset()
        
        return qs.filter(
            Q(title__icontains=search_term)|
            Q(description__icontains=search_term)
        ).order_by("-id")
    
    def get_context_data(self):
        ctx = super().get_context_data()

        ctx.update({
            "search_term": self.request.GET.get('q', '')
        })
        return ctx

class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = 'recipe.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx.update({"is_detail_page": True})
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

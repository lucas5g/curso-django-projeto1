from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from tags.admin import TagInline
from tags.models import Tag
from .models import Category, Recipe

# class TagInline(GenericStackedInline):
#     model = Tag
#     fields = 'name',
#     extra = 1

class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published']
    list_display_links = ['id', 'title']
    search_fields = ['id', 'title', 'description']
    list_filter = ['category', 'author', 'is_published', 'preparation_steps_is_html']
    list_per_page = 10
    list_editable = ['is_published']
    ordering = '-id',
    prepopulated_fields = {
        "slug":["title"]
    }
    # inlines = [TagInline]

admin.site.register(Category, CategoryAdmin)
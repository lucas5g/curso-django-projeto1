from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import Concat
from django.db.models.query import F, Value
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from tags.models import Tag
from collections import defaultdict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F("author__first_name"), Value("("),
                F("author__username"), Value(')')
            )
        )

# Create your models here.
class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:recipe", args=(self.id,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if not recipe_from_db:
            return 
        
        if recipe_from_db.pk != self.pk:
            error_messages['title'].append('Found recipes with the same title...')

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

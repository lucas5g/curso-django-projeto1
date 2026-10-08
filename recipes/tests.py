from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe, User
from unittest import skip 
from django.core.exceptions import ValidationError 

# Create your tests here.
class RecipeURLsTest(TestCase):


    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')


    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_details_url_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEqual(url, '/recipes/1')

class RecipeViewsTest(TestCase):

    def setUp(self):
        category = Category.objects.create(name="Category")
        author = User.objects.create_user(
            first_name="user",
            last_name="name",
            username="username",
            password="123456",
            email="username@mail.com"
        )

        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title="Recipe Title",
            description="Recipe Description",
            slug="recipe-title",
            preparation_time=10,
            preparation_time_unit="minutes",
            servings=5,
            servings_unit="portions",
            preparation_steps="Recipe Preparation Steps",
            is_published=True,
        )

    def test_recipe_home_views_function_is_correct(self):
        view = resolve("/")
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve("/recipes/category/1/")
        self.assertIs(view.func, views.category)

    def test_recipe_details_view_function_is_correct(self):
        view = resolve("/recipes/1")
        self.assertIs(view.func, views.recipe)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipe(self):
        Recipe.objects.filter(pk=1).delete()

        response = self.client.get(reverse('recipes:home'))

        self.assertIn('No recipes found here',
                      response.content.decode('utf-8'))

    def test_recipe_category_view_funcion_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)


    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 404})
        )
        self.assertEqual(response.status_code, 404)


    def test_recipe_home_template_loads_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context = response.context['recipes']
        self.assertIn('Recipe Title', content)
        self.assertIn('10 minutes', content)
        self.assertIn('5 portions', content)
        self.assertEqual(len(response_context), 1)


    def test_recip_home_template_dont_load_recipes_not_published(self):

        recipe = Recipe.objects.get(pk=1)
        recipe.is_published = False
        recipe.save()

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'No recipes found here',
            response.content.decode('utf-8')
        )

class RecipeModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Category")
        author = User.objects.create_user(
            first_name="user",
            last_name="name",
            username="username",
            password="123456",
            email="username@mail.com"
        )

        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title="Recipe Title",
            description="Recipe Description",
            slug="recipe-title",
            preparation_time=10,
            preparation_time_unit="minutes",
            servings=5,
            servings_unit="portions",
            preparation_steps="Recipe Preparation Steps",
            is_published=True,
        )

    def test_recipe_title_raise_error_if_title_has_more_then_65_chars(self):
        recipe = Recipe.objects.filter(pk=1).first()
        recipe.title = 'A' * 70 

        with self.assertRaises(ValidationError):
            recipe.full_clean()  # save() não valida; full_clean() checa max_length

    
    def test_recipe_fields_max_lenght(self):
        fields = [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
            ('slug', 65),
        ]

        for field, max_lenght in fields:
            # subTest mostra qual campo falhou, sem parar no primeiro
            with self.subTest(field=field, max_lenght=max_lenght):
                recipe = Recipe.objects.filter(pk=1).first()
                setattr(recipe, field, 'A' * (max_lenght + 1))
                with self.assertRaises(ValidationError):
                    recipe.full_clean()

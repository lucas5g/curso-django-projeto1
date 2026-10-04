from django.test import TestCase
from django.urls import reverse, resolve

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
    def test_recipe_home_views_function_is_correct(self):
        view = resolve("/")
        self.assertIs(view.func, view.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve("/recipes/category/1/")
        self.assertIs(view.func, view.category)
    
    def test_recipe_details_view_function_is_correct(self):
        view = resolve("/recipes/1")
        self.assertIs(view.func, view.recipe)

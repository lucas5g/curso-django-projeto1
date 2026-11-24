from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe, User
from unittest import skip
from django.core.exceptions import ValidationError
from unittest.mock import patch
from rest_framework import test


# Create your tests here.
class RecipeURLsTest(TestCase):

    def test_recipe_home_url_is_correct(self):
        url = reverse("recipes:home")
        self.assertEqual(url, "/")

    def test_recipe_category_url_is_correct(self):
        url = reverse("recipes:category", kwargs={"category_id": 1})
        self.assertEqual(url, "/recipes/category/1/")

    def test_recipe_details_url_is_correct(self):
        url = reverse("recipes:recipe", kwargs={"pk": 1})
        self.assertEqual(url, "/recipes/1")

    def test_recipe_search_url_is_correct(self):
        url = reverse("recipes:search")
        self.assertEqual(url, "/recipes/search/")


class RecipeViewsTest(TestCase):

    def setUp(self):
        category = Category.objects.create(name="Category")
        author = User.objects.create_user(
            first_name="user",
            last_name="name",
            username="username",
            password="123456",
            email="username@mail.com",
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
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve("/recipes/category/1/")
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_details_view_function_is_correct(self):
        view = resolve("/recipes/1")
        self.assertIs(view.func.view_class, views.RecipeDetail)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipe(self):
        Recipe.objects.filter(pk=1).delete()

        response = self.client.get(reverse("recipes:home"))

        self.assertIn("No recipes found here", response.content.decode("utf-8"))

    def test_recipe_category_view_funcion_is_correct(self):
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse("recipes:recipe", kwargs={"pk": 1}))
        self.assertIs(view.func.view_class, views.RecipeDetail)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):

        response = self.client.get(reverse("recipes:recipe", kwargs={"pk": 404}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_home_template_loads_recipes(self):
        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode("utf-8")
        response_context = response.context["recipes"]
        self.assertIn("Recipe Title", content)
        self.assertIn("10 minutes", content)
        self.assertIn("5 portions", content)
        self.assertEqual(len(response_context), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):

        recipe = Recipe.objects.get(pk=1)
        recipe.is_published = False
        recipe.save()

        response = self.client.get(reverse("recipes:home"))

        self.assertIn("No recipes found here", response.content.decode("utf-8"))

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse("recipes:search") + "?q=teste")

        self.assertTemplateUsed(response, "search.html")

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse("recipes:search"))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse("recipes:search") + "?q=Teste"
        response = self.client.get(url)

        self.assertIn("Search for &quot;Teste&quot;", response.content.decode("utf-8"))

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = "This is recipe one"
        title2 = "This is recipe two"

        recipe1 = Recipe.objects.get(pk=1)
        recipe1.title = title1
        recipe1.save()

        recipe2 = Recipe.objects.create(
            category=Recipe.objects.get(pk=1).category,
            author=Recipe.objects.get(pk=1).author,
            title=title2,
            description="Recipe Description",
            slug="recipe-title-2",
            preparation_time=10,
            preparation_time_unit="minutes",
            servings=5,
            servings_unit="portions",
            preparation_steps="Recipe Preparation Steps",
            is_published=True,
        )
        recipe2.save()

        search_url = reverse("recipes:search")

        response1 = self.client.get(f"{search_url}?q={title1}")
        response2 = self.client.get(f"{search_url}?query={title2}")
        response_both = self.client.get(f"{search_url}?q=this")

        self.assertIn(recipe1, response1.context["recipes"])
        self.assertNotIn(recipe2, response1.context["recipes"])

        self.assertIn(recipe1, response_both.context["recipes"])
        self.assertIn(recipe2, response_both.context["recipes"])

    def test_recipe_home_is_paginated(self):
        for i in range(8):
            recipe = Recipe.objects.create(
                category=Recipe.objects.get(pk=1).category,
                author=Recipe.objects.get(pk=1).author,
                title=f"Recipe {i}",
                description="Recipe Description",
                slug=f"recipe-{i}",
                preparation_time=10,
                preparation_time_unit="minutes",
                servings=5,
                servings_unit="portions",
                preparation_steps="Recipe Preparation Steps",
                is_published=True,
            )
            recipe.save()

        with patch.object(views.RecipeListViewHome, "paginate_by", 3):
            response = self.client.get(reverse("recipes:home"))
            recipes = response.context["recipes"]
            paginator = recipes.paginator
            self.assertEqual(paginator.num_pages, 3)

            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 3)

    # def test_make_pagination_uses_page_


class RecipeModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Category")
        author = User.objects.create_user(
            first_name="user",
            last_name="name",
            username="username",
            password="123456",
            email="username@mail.com",
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
        recipe.title = "A" * 70

        with self.assertRaises(ValidationError):
            recipe.full_clean()  # save() não valida; full_clean() checa max_length

    def test_recipe_fields_max_lenght(self):
        fields = [
            ("title", 65),
            ("description", 165),
            ("preparation_time_unit", 65),
            ("servings_unit", 65),
            ("slug", 65),
        ]

        for field, max_lenght in fields:
            # subTest mostra qual campo falhou, sem parar no primeiro
            with self.subTest(field=field, max_lenght=max_lenght):
                recipe = Recipe.objects.filter(pk=1).first()
                setattr(recipe, field, "A" * (max_lenght + 1))
                with self.assertRaises(ValidationError):
                    recipe.full_clean()

    def test_recipe_preparations_steps_is_html_is_false_by_default(self):
        recipe = Recipe.objects.filter(pk=1).first()
        recipe.preparation_steps_is_html = False
        # recipe.save()

        self.assertFalse(recipe.preparation_steps_is_html)

    def test_recipe_is_published_is_false_by_default(self):
        recipe = Recipe.objects.filter(pk=1).first()
        recipe.is_published = False
        self.assertFalse(recipe.is_published)


class RecipeAPIV2Test(test.APITestCase):

    accessToken=''

    def setUp(self):
        category_1 = Category.objects.create(name="Café da manhã")
        category_2 = Category.objects.create(name="Almoço")

        for i in range(2):
            User.objects.create_user(
                first_name=f"user{i}",
                last_name=f"name{i}",
                username=f"username{i}",
                password="123456",
                email=f"username{i}@mail.com",
            )

        author = User.objects.get(pk=1)
        

        Recipe.objects.create(
            category=category_1,
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

        Recipe.objects.create(
            category=category_2,
            author=author,
            title="Recipe Title 2",
            description="Recipe Description",
            slug="recipe-title-2",
            preparation_time=10,
            preparation_time_unit="minutes",
            servings=5,
            servings_unit="portions",
            preparation_steps="Recipe Preparation Steps",
            is_published=True,
        )

        response = self.client.post(
            "/recipes/api/token/", data={"username": author.username, "password": "123456"}
        )
        
        self.accessToken = response.data["access"]

    def test_recipe_api_list_returns_status_code_200(self):
        api_url = reverse("recipes:recipe-api-list")
        response = self.client.get(api_url)

        self.assertEqual(response.status_code, 200)

    @patch("recipes.views.api.RecipeAPIv2Pagination.page_size", new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_recipes = 7

        for i in range(wanted_recipes):
            category = Category.objects.create(name=f"Category {i}")
            author = User.objects.create_user(
                first_name=f"user{i}",
                last_name=f"name{i}",
                username=f"username{i}",
                password="123456",
                email=f"username{i}@mail.com",
            )

            recipe = Recipe.objects.create(
                category=category,
                author=author,
                title=f"Recipe Title {i}",
                description="Recipe Description",
                slug=f"recipe-title-{i}",
                preparation_time=10,
                preparation_time_unit="minutes",
                servings=5,
                servings_unit="portions",
                preparation_steps="Recipe Preparation Steps",
                is_published=True,
            )
        response = self.client.get(reverse("recipes:recipe-api-list"))
        qtd_recipes_received = len(response.data.get("results"))
        self.assertEqual(wanted_recipes, qtd_recipes_received)

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipe = Recipe.objects.get(pk=1)
        recipe.is_published = False
        recipe.save()
        response = self.client.get(reverse("recipes:recipe-api-list"))

        self.assertEqual(response.data["count"], 0)

    def test_recipe_api_list_loads_recipes_by_category_id(self):
        category_id = 2
        category = Category.objects.get(pk=category_id)

        response = self.client.get(
            reverse("recipes:recipe-api-list") + f"?category_id={category_id}"
        )

        self.assertEqual(response.data["results"][0]["category"], category.name)

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        response = self.client.post(reverse("recipes:recipe-api-list"))

        self.assertEqual(response.status_code, 401)

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        
        response = self.client.post(
            reverse("recipes:recipe-api-list"),
            data={
                "category": 1,
                "author": 1,
                "title": "Recipe Title",
                "description": "Recipe Description",
                "slug": "recipe-title",
                "preparation_time": 10,
                "preparation_time_unit": "minutes",
                "servings": 5,
                "servings_unit": "portions",
                "preparation_steps": "Recipe Preparation Steps",
                "is_published": True,
            },
            HTTP_AUTHORIZATION=f'Bearer {self.accessToken}'
        )

        self.assertEqual(response.status_code, 201)

    def test_recipe_api_list_update_recipe(self):

        response = self.client.patch(
            "/api/recipes/1/",
            data={
                "category": 1,
                "author": 1,
                "title": "Recipe Title Updated",
                "description": "Recipe Description",
                "slug": "recipe-title",
                "preparation_time": 10,
                "preparation_time_unit": "minutes",
                "servings": 5,
                "servings_unit": "portions",
                "preparation_steps": "Recipe Preparation Steps",
                "is_published": True,
            },
            HTTP_AUTHORIZATION=f'Bearer {self.accessToken}'
        )

        self.assertEqual(response.status_code, 200)

    def test_recipe_api_list_dont_update_recipe_with_other_author(self):
        user2 = User.objects.get(pk=2)
        response = self.client.post(
            "/recipes/api/token/", data={"username": "username1", "password": "123456"}
        )

        access_token = response.data["access"]

        response = self.client.patch(
            "/api/recipes/1/",
            data={
                "category": 1,
                "author": 2,
                "title": "Recipe Title Updated",
                "description": "Recipe Description",
                "slug": "recipe-title",
                "preparation_time": 10,
                "preparation_time_unit": "minutes",
                "servings": 5,
                "servings_unit": "portions",
                "preparation_steps": "Recipe Preparation Steps",
                "is_published": True,
            },
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        self.assertEqual(response.status_code, 403)

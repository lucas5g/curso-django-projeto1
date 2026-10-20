# from django.test import TestCase
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from parameterized import parameterized
from django.urls import reverse
from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand(
        [
            # ('username', 'Username'),
            # ('email','E-mail'),
            ("first_name", "Type your FirstName here")
        ]
    )
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand(
        [
            (
                "username",
                "Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.",
            ),
            ("email", "The e-mail must be valid."),
            ("password", "Use at least 8 characters, including an uppercase letter, a lowercase letter, and a number.")
            # ("password", "Password must have at least one uppercase letter, and one number. The length should be at least 8 characters."),
        ]
    )
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand(
        [
            (
                "username",
                "Username",
            ),
            ("first_name", "First Name"),
            ("last_name", "Last Name"),
            ("email", "E-mail"),
            ("password", "Password")
            # ("password", "Password must have at least one uppercase letter, and one number. The length should be at least 8 characters."),
        ]
    )
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)

class AuthorRegisterFormTestCase(DjangoTestCase):
    def setUp(self):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password':'Strong@123',
            'passowrd2': 'Strong@123'
        }

    @parameterized.expand([
        ('username', 'Este campo é obrigatório'),
        ('first_name', 'Este campo é obrigatório'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

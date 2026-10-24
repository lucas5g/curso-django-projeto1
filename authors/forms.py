import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from recipes.models import Recipe


def strong_password(password):
    regex = re.compile(r"(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?=.*\Z).{8,}$")

    if not regex.match(password):
        raise ValidationError(
            "Password must have at least one uppercase letter, "
            "one lowercase letter and one number. The length should be "
            "at least 8 characters.",
            code="Invalid",
        )


class RegisterForm(forms.ModelForm):

    username = forms.CharField(
        help_text=(
            "Username must have letters, numbers or one of those @.+-_."
            "The lenght should be between 4 and 150 characters."
        ),
        error_messages={
            "required": "This field must not be empty",
            "min_length": "Username must have at least 4 characters",
            "max_length": "Username must have less than 150 characters",
        },
        min_length=4,
        max_length=150,
    )

    password = forms.CharField(
        required=True,
        validators=[strong_password],
        help_text=(
            "Use at least 8 characters, including an uppercase letter, "
            "a lowercase letter, and a number."
        ),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Type your Password here",
            }
        ),
        label="Password",
        error_messages={"required": "Password must not be empty"},
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat your password",
            }
        ),
        label="Password Confirmation",
        error_messages={"required": "Please, repeat your password"},
    )

    class Meta:

        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

        labels = {
            # 'username': 'Username',
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "E-mail",
        }

        help_texts = {
            "email": "The e-mail must be valid.",
            "username": (
                "Username must have letters, numbers or one of those @.+-_."
                "The lenght should be between 4 and 150 characters."
            ),
        }

        error_messages = {
            "first_name": {"required": "Write your first name"},
            "last_name": {"required": "Write your last name"},
            "email": {"required": "Email is required"},
        }

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Type your FirstName here",
                    "class": "input text-input outra",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError("User e-mail is already in use", code="invalid")
        return email

    def clean(self):
        clean_data = super().clean()

        password = clean_data.get("password")
        password2 = clean_data.get("password2")

        if password != password2:

            password_confirmation_error = ValidationError(
                "Password and password2 must be equal", code="invalid"
            )

            raise ValidationError(
                {
                    "password": password_confirmation_error,
                    "password2": password_confirmation_error,
                }
            )

        # return


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Type your Username here",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Type your Password here",
            }
        )
    )


class AuthorRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "preparation_steps",
            "cover",
        ]

        widgets = {
            "preparation_steps": forms.Textarea(
                attrs={"class": "span-2"}
            ),
            "cover": forms.ClearableFileInput(
                attrs={"class":"span-2"}
            )
        }
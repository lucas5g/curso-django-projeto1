import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def strong_password(password):
    regex = re.compile(r'(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?=.*\Z).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number. The length should be'
            'at least 8 characters.',
        ),
            code='Invalid'
        )

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        validators=[strong_password],
        help_text=(
            'Use at least 8 characters, including an uppercase letter, '
            'a lowercase letter, and a number.'
        ),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your Password here',
        }),
        label='Password'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'E-mail',
        }

        help_texts = {
            'email': 'The e-mail must be valid.'
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty.',
                'invalid': 'This field is invalid.'
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your FirstName here',
                'class': 'input text-input outra'
            }),
        }

    def clean(self):
        clean_data = super().clean()

        password = clean_data.get('password')
        password2 = clean_data.get('password2')

        if password != password2:

            password_confirmation_error = ValidationError(
                'Password and password2 must be the equal',
                code='invalid'
            )

            raise ValidationError({
                'password': password_confirmation_error,
                'password2': password_confirmation_error,

            })

        # return

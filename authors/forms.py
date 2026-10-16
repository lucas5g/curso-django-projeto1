from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
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
            'email': 'Email',
            'password': 'Password',
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
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your Password here',
            })
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if '123' in data:
            raise ValidationError(
                'Não digite "123" no campo password.',
                code='invalid_password'
            )
        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'teste' in data:
            raise ValidationError(
                'Não digite %(values)s no campo first name',
                code='invalid',
                params={'values': data}
            )

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

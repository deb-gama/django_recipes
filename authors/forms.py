from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def add_attr(field, attr_name, attr_new_value):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_value}'.strip()

def add_placeholder(field, placeholder_value):
    field.widget.attrs['placeholder'] = placeholder_value


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$')

    if not regex.match(password):
       raise ValidationError((
           'Password must have at least one uppercase letter,'
           'one lowercase letter and one number. The length should be'
           'at least 8 characters'
       ),
       code = 'invalid'
       )

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'],'Your username')
        add_placeholder(self.fields['email'],'Ex: your_best_email@email.com')
        add_placeholder(self.fields['first_name'],'Ex: John / Jane')
        add_placeholder(self.fields['last_name'],'Ex: Doe')


    confirm_password = forms.CharField(
        required=True,
        widget = forms.PasswordInput(attrs = {
        'placeholder': 'Confirm your password'
        }),
        error_messages={
        'required': 'You must have to confirm your password'
        },
    )

    password = forms.CharField(
        required=True,
        widget = forms.PasswordInput(attrs = {
        'placeholder': 'Your password'
        }),
        error_messages={
        'required': 'This field must not be empty'
        },
        validators = [strong_password]
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }

        help_texts = {
            'email': 'The email must be valid',
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code = 'invalid',
                params = {'value': '"atenção"'}
            )

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code = 'invalid',
                params = {'value': '"John Doe"'}
            )

        return data


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            password_error = ValidationError(
            'The passwords must be equal',
            code = 'invalid'
            )

            raise ValidationError({
                'confirm_password': [password_error],
                'password': [
                    password_error,
                ]
            })

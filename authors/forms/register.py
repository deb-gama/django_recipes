from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from recipes.utils.django_forms import (
    add_placeholder,
    strong_password,
    add_attr
)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Ex: your_best_email@email.com')
        add_placeholder(self.fields['first_name'], 'Ex: John / Jane')
        add_placeholder(self.fields['last_name'], 'Ex: Doe')

    first_name = forms.CharField(
        error_messages={'required': 'Type your First Name'},
        required=True,
        label='First Name',
    )

    last_name = forms.CharField(
        error_messages={'required': 'Type your Last Name'},
        required=True,
        label='Last Name',
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password'
        }),
        error_messages={
            'required': 'Please, repeat your password'
        },
        label='Confirm Password'
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        label='Password',
        validators=[strong_password],

    )

    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your e-mail'
        }),
        error_messages={
            'required': 'E-mail is required'
        },
        label='E-mail',
        help_text='The email must be valid'
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
            'username': 'Username',
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
                code='invalid',
                params={'value': '"atenção"'}
            )

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code='invalid',
                params={'value': '"John Doe"'}
            )

        return data


    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email = email).exists()

        if exists:
            raise ValidationError(
                'This email is already in use',
                code='invalid'
            )

        return email


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            password_error = ValidationError(
                'The passwords must be equal',
                code='invalid'
            )

            raise ValidationError({
                'confirm_password': [password_error],
                'password': [
                    password_error,
                ]
            })



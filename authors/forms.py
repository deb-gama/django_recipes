from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def add_attr(field, attr_name, attr_new_value):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_value}'.strip()


def add_placeholder(field, placeholder_value):
    field.widget.attrs['placeholder'] = placeholder_value

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'],'Your username')
        add_placeholder(self.fields['email'],'Ex: youremail@email.com')
        add_placeholder(self.fields['first_name'],'Ex: Jon')
        add_placeholder(self.fields['last_name'],'Ex: Doe')




    confirm_password = forms.CharField(
        required=True,
        widget = forms.PasswordInput(attrs = {
        'placeholder': 'Confirm your password'
        }),
        error_messages={
        'required': 'You must have to confirm your password'
        },
        help_text=('Passwords must be equals')
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

        widgets = {
            'username': forms.TextInput(attrs = {
            'class': 'input text-input'
            }),
            'password': forms.PasswordInput(attrs = {
            'placeholder': 'Type your password here',
            }),
        }


    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite atenção no campo password',
                code = 'invalid',
            )

        return data


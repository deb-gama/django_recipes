from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Ex: your_best_email@email.com'),
        ('first_name', 'Ex: John / Jane'),
        ('last_name', 'Ex: Doe'),
        ('password', 'Your password'),
        ('confirm_password', 'Confirm your password'),
    ])
    def test_placeholders_is_correct(self, field, placeholder):
        form = RegisterForm()
        placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, placeholder)
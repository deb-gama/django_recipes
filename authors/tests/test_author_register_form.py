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
    def test_fields_placeholders(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
       ('email', 'The email must be valid'),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text

        self.assertEqual(current, needed)

    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('username','Username'),
        ('email','E-mail'),
        ('password','Password'),
        ('confirm_password', 'Confirm Password'),
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label

        self.assertEqual(current_label, label)




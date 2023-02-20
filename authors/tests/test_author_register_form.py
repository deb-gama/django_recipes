from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


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
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('confirm_password', 'Confirm Password'),
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label

        self.assertEqual(current_label, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'mail@mail.com',
            'password': 'StrongP@ssword1',
            'confirm_password': 'StrongP@ssword1'
        }
        return super().setUp()

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Type your First Name'),
        ('last_name', 'Type your Last Name'),
        ('password', 'Password must not be empty'),
        ('confirm_password', 'Please, repeat your password'),
        ('email', 'E-mail is required'),
    ])
    def test_fields_cannot_be_empty(self, field, message):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(message, response.context['form'].errors.get(field))


    def test_password_field_have_lower_upper_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        message = 'Password must have at least one uppercase letter,one lowercase letter and one number. The length should beat least 8 characters'

        self.assertIn(message, response.context['form'].errors.get('password'))
        self.assertIn(message, response.content.decode('utf-8'))


    def test_password_field_have_lower_upper_letters_and_numbers_should_not_raise_error(self):
        self.form_data['password'] = 'Abc12300'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        message = 'Password must have at least one uppercase letter,one lowercase letter and one number. The length should beat least 8 characters'

        self.assertNotIn(message, response.context['form'].errors.get('password'))
        self.assertNotIn(message, response.content.decode('utf-8'))


    def test_password_field_and_confirm_password_are_equal(self):
        self.form_data['password'] = 'Abc12300'
        self.form_data['confirm_password'] = 'Abc1230022'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        message = 'The passwords must be equal'

        self.assertIn(message, response.context['form'].errors.get('password'))
        self.assertIn(message, response.content.decode('utf-8'))


    def test_password_and_confirm_your_password_should_not_raise_an_error_if_the_values_are_equal(self):
        self.form_data['password'] = 'Abc12300'
        self.form_data['confirm_password'] = 'Abc12300'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        message = 'The passwords must be equal'

        self.assertNotIn(message, response.content.decode('utf-8'))

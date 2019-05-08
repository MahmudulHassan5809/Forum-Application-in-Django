from django.test import TestCase
from django.urls import reverse,resolve
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from ..views import signup
from ..forms import SignUpForm

# Create your tests here.
class signUpTests(TestCase):

	def setUp(self):
		url = reverse('accounts:signup')
		self.response = self.client.get(url)

	def test_signup_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_signup_url_resolves_signup_view(self):
		view = resolve('/accounts/signup/')
		self.assertEquals(view.func, signup)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, UserCreationForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<input', 7)
		self.assertContains(self.response, 'type="text"', 3)
		self.assertContains(self.response, 'type="email"', 1)
		self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
	def setUp(self):
		url = reverse('accounts:signup')
		data = {
			'first_name': 'jhon',
			'last_name': 'Doe',
			'email': 'jhon@gmail.com',
            'username': 'john',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
		}
		self.response = self.client.post(url, data)
		self.home_url = reverse('boards:home')

	def test_redirection(self):
		self.assertRedirects(self.response, self.home_url)

	def test_user_creation(self):
		self.assertTrue(User.objects.exists())

	def test_user_authentication(self):
		response = self.client.get(self.home_url)
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
	def setUp(self):
		url = reverse('accounts:signup')
		self.response = self.client.post(url, {})

	def test_signup_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)

	def test_dont_create_user(self):
		self.assertFalse(User.objects.exists())

class SignUpFormTest(TestCase):
	def test_form_has_fields(self):
		form = SignUpForm()
		expected = ['first_name','last_name','username', 'email', 'password1', 'password2',]
		actual = list(form.fields)
		self.assertSequenceEqual(expected, actual)

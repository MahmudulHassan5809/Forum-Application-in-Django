from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
	email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

	first_name = forms.CharField(max_length=254, required=True)
	last_name = forms.CharField(max_length=254, required=True)

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True

	class Meta:
		model = User
		fields = ('first_name','last_name','username', 'email', 'password1', 'password2')

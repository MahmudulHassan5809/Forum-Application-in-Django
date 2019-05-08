from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import login as auth_login
from django.http import HttpResponse,Http404
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm


from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

# Create your views here.
def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			auth_login(request,user)
			return redirect('boards:home')
	else:
		form = SignUpForm()

	context = {
		'title' : 'Register',
		'form' : form
	}
	return render(request,'signup.html',context)


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
	model = User
	fields = ('first_name','last_name','email',)
	template_name = 'my_account.html'
	success_url = reverse_lazy('accounts:my_account')

	def get_form(self, form_class=None):
		form = super(UserUpdateView, self).get_form(form_class)
		form.fields['first_name'].required = True
		form.fields['last_name'].required = True
		form.fields['email'].required = True
		return form

	def get_object(self):
		return self.request.user

	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return redirect('accounts:my_account')

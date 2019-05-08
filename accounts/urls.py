from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
	path('signup/',views.signup,name='signup'),
	path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
	path('password/',auth_views.PasswordChangeView.as_view(template_name='password_change.html'),name='password_change'),
	path('password/done/',auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),name='password_change_done'),
	path('my_account/',views.UserUpdateView.as_view(),name='my_account'),
	path('logout/',auth_views.LogoutView.as_view(),name='logout'),
]

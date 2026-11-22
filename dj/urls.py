from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from myapp import views
from myapp.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(
        template_name='login.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True,
    ), name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),  # POST only
]

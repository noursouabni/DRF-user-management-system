"""
URL configuration for FormAI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users import views
from django.contrib.auth import views as auth_views
from users.views import SignupAPIView, home,signup_page,UserProfileAPIView
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', TemplateView.as_view(template_name='users/homepage.html'), name='homepage'),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('signup/', SignupAPIView.as_view(), name='signup'), # DRF API endpoint
    path('signup-page/', TemplateView.as_view(template_name='users/signup.html'), name='signup_page'),
    path('login-page/', TemplateView.as_view(template_name='users/login.html'), name='login_page'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
]   


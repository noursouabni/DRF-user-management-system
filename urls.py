'''from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import api_signup, signup
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('api/signup/', api_signup, name='api_signup'),  # API-based signup
    path('signup/', signup, name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),

]'''
from django.urls import path
from .views import SignupAPIView, UserAPIView,LoginAPIView,UserProfileAPIView
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from django.views.generic import TemplateView


urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('users/', UserAPIView.as_view()),  # For GET all users and POST
    path('users/<int:id_user>/', UserAPIView.as_view()), 
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login endpoint
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('login/', LoginAPIView.as_view(), name='login'), 
    path('profile/', UserProfileAPIView.as_view(), name='profile_api'),  #drf
    path('profile-page/', TemplateView.as_view(template_name='users/userprofile.html'), name='profile_page'),  #html 
    path('login-user/', TemplateView.as_view(template_name='users/login_user.html'), name='login-user'),  #html 
    path('profile-user/', TemplateView.as_view(template_name='users/profile_user.html'), name='profile_user'),  #html 
    path('signup-user/', TemplateView.as_view(template_name='users/signup_user.html'), name='signup_user'),
    path('login-admin/', TemplateView.as_view(template_name='users/login-admin.html'), name='login-admin'),
    path('signup-admin/', TemplateView.as_view(template_name='users/signup-admin.html'), name='signup-admin'),
    
]
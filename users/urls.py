"""
URL configuration for infohub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from . import views
from django.urls import path

urlpatterns = [
    # path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
        # mail activation
    path("activate/<uidb64>/<token>/", views.activate, name='activate'),
    path("reset_password_validation/<uidb64>/<token>/", views.reset_password_validation, name='reset_password_validation'),
    path("reset_password/", views.reset_password, name='reset_password'),
]


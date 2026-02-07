from . import views
from django.urls import path

urlpatterns = [
    # path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('other_user_profile/<int:pk>/', views.other_user_profile, name='other_user_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_categories/', views.dashboard_categories, name='dashboard_categories'),
    path('dashboard_stories/', views.dashboard_stories, name='dashboard_stories'),
    path('dashboard_users/', views.dashboard_users, name='dashboard_users'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('adduser/', views.adduser, name='adduser'),
    path('edituser/<int:pk>/', views.edituser, name='edituser'),
    path('deleteuser/<int:pk>/', views.deleteuser, name='deleteuser'),
        # mail activation
    path("activate/<uidb64>/<token>/", views.activate, name='activate'),
    path("reset_password_validation/<uidb64>/<token>/", views.reset_password_validation, name='reset_password_validation'),
    path("reset_password/", views.reset_password, name='reset_password'),
]
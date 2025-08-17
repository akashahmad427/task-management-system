from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # User management
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.UserUpdateView.as_view(), name='profile-update'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user-update'),
] 
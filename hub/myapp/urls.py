from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Homepage
    path('', views.homepage_view, name='homepage'),

    # Authentication Routes
    path('register/', views.register, name='register'),  # User Registration
    path('login/', auth_views.LoginView.as_view(template_name='hub/auth.html'), name='login'),  # User Login
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Logout

    # Projects
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/filter/', views.filter_projects_view, name='filter_projects'),
    path('api/filter-projects/', views.filter_projects, name='filter_projects_api'),
    path('projects/', views.project_list, name='project_list'),

    # Project Suggestion
    path('suggest-project/', views.suggest_project, name='suggest_project'),

    # Profile
    path('profile/', views.profile, name='profile'),
]

# Serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ADDED: Serve static files in development (only recommended when DEBUG = True)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

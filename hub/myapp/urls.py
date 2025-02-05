from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),  # Homepage
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('create/', views.create_project, name='create_project'),  # Correct name for the Create Project page
    path('register/', views.register, name='register'),  # Register page
    path('login/', auth_views.LoginView.as_view(template_name='hub/login.html'), name='login'),  # Add login route
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Optional logout route
    path('projects/filter/', views.filter_projects_view, name='filter_projects'),  # Filter projects
    path('filter-projects/', views.filter_projects, name='filter_projects_api'),  # AJAX endpoint
    path("filter-projects/", views.project_list, name="project_list"),
    path('logout/', views.logout_view, name='logout'),
    ]

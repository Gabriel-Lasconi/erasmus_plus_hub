from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.homepage_view, name='homepage'),  # Homepage
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('register/', views.register, name='auth'),  # Register page
    path('auth/', auth_views.LoginView.as_view(template_name='hub/auth.html'), name='auth'),  # Add login route
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Optional logout route
    path('projects/filter/', views.filter_projects_view, name='filter_projects'),  # Filter projects
    path('filter-projects/', views.filter_projects, name='filter_projects_api'),  # AJAX endpoint
    path("filter-projects/", views.project_list, name="project_list"),
    path('logout/', views.logout_view, name='logout'),
    path('suggest-project/', views.suggest_project, name='suggest_project'),
    path("profile/", views.profile, name="profile"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


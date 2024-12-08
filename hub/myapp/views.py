from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from django.http import HttpResponseForbidden
from .forms import RegisterForm
from django.http import JsonResponse

def homepage_view(request):
    return render(request, 'hub/homepage.html')

# def project_list(request):
#     projects = Project.objects.all()
#     return render(request, 'hub/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'hub/project_detail.html', {'project': project})

@login_required
def create_project(request):
    if not request.user.is_staff:  # Ensure the user is an admin
        return HttpResponseForbidden("You are not authorized to access this page.")  # Restrict access

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to the homepage after saving
    else:
        form = ProjectForm()
    return render(request, 'hub/create_project.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegisterForm()
    return render(request, 'hub/register.html', {'form': form})

def filter_projects(request):
    # Get filter parameters
    project_type = request.GET.get('type', '')
    country = request.GET.get('country', '')
    deadline = request.GET.get('deadline', '')

    # Filter projects
    projects = Project.objects.all()

    if project_type:
        projects = projects.filter(type=project_type)  # Ensure 'type' exists in the model
    if country:
        projects = projects.filter(country=country)  # Ensure 'location' exists in the model
    if deadline:
        projects = projects.filter(deadline__lte=deadline)  # Ensure 'deadline' exists in the model

    # Serialize projects to JSON format
    project_list = list(projects.values('id', 'name', 'country', 'type', 'deadline'))
    return JsonResponse(project_list, safe=False)

def filter_projects_view(request):
    return render(request, 'hub/filter_projects.html')

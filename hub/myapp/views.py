# myapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import CreateProjectForm
from django.http import HttpResponseForbidden
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import logout


def homepage_view(request):
    return render(request, 'hub/homepage.html')

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'hub/project_detail.html', {'project': project})

@login_required
def create_project(request):
    if not request.user.is_staff:  # Ensure the user is an admin
        return HttpResponseForbidden("You are not authorized to access this page.")  # Restrict access

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to the homepage after saving
    else:
        form = CreateProjectForm()
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


from django.http import JsonResponse
from .models import Project


def filter_projects(request):
    projects = Project.objects.filter(approved=True)  # Ensure only approved projects are included

    type_filter = request.GET.get("type", "")
    country_filter = request.GET.get("country", "")
    deadline_filter = request.GET.get("deadline", "")

    if type_filter:
        projects = projects.filter(type=type_filter)
    if country_filter:
        projects = projects.filter(country=country_filter)
    if deadline_filter:
        projects = projects.filter(deadline__lte=deadline_filter)  # Ensure filtering by deadline

    # Convert queryset to a list of dictionaries
    project_list = list(projects.values("id", "name", "country", "deadline", "submitted_by", "approved"))

    return JsonResponse(project_list, safe=False)


def filter_projects_view(request):
    return render(request, 'hub/filter_projects.html')

@login_required
def suggest_project(request):
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.submitted_by = request.user  # ✅ Assign user properly
            project.approved = request.user.is_staff  # ✅ Auto-approve if admin
            project.save()
            return redirect("/")
    else:
        form = CreateProjectForm()

    return render(request, "hub/suggest_project.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to home page after logout
# def project_list(request):
#     projects = CreateProjectForm.objects.filter(approved=True)
#
#     project_type = request.GET.get("type")
#     country = request.GET.get("country")
#     deadline = request.GET.get("deadline")
#
#     if project_type:
#         projects = projects.filter(project_type=project_type)
#     if country:
#         projects = projects.filter(country=country)
#     if deadline:
#         projects = projects.filter(deadline__lte=deadline)
#
#     # AJAX response
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         data = list(projects.values("id", "title", "country", "deadline", "submitted_by"))
#         return JsonResponse(data, safe=False)
#
#     return render(request, "hub/filter_projects.html", {"projects": projects})

def project_list(request):
    projects = Project.objects.filter(approved=True)  # ✅ Only show approved projects
    return render(request, "hub/filter_projects.html", {"projects": projects})

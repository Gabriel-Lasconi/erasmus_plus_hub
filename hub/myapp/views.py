# myapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CreateProjectForm
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Certification, Badge
from .forms import UserUpdateForm, ProfileUpdateForm

def homepage_view(request):
    return render(request, 'hub/homepage.html')

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'hub/project_detail.html', {'project': project})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auth')
    else:
        form = RegisterForm()
    return render(request, 'hub/auth.html', {'form': form})


from django.http import JsonResponse
from .models import Project


def filter_projects(request):
    projects = Project.objects.filter(approved=True)

    type_filter = request.GET.get("type", "")
    country_filter = request.GET.get("country", "")
    deadline_filter = request.GET.get("deadline", "")

    if type_filter:
        projects = projects.filter(type=type_filter)
    if country_filter:
        projects = projects.filter(country=country_filter)
    if deadline_filter:
        projects = projects.filter(deadline__lte=deadline_filter)

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
            project.submitted_by = request.user.username
            project.approved = request.user.is_staff
            project.save()
            return redirect("/")
    else:
        form = CreateProjectForm()

    return render(request, "hub/suggest_project.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')

def project_list(request):
    projects = Project.objects.filter(approved=True)
    return render(request, "hub/filter_projects.html", {"projects": projects})

@login_required
def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    certifications = Certification.objects.filter(user=request.user)
    badges = request.user.badges.all()  # ✅ Works for both ForeignKey & ManyToManyField

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user_profile)

    return render(request, 'hub/profile.html', {
        "user_form": user_form,
        "profile_form": profile_form,
        "certifications": certifications,
        "badges": badges,
    })

def award_badge(user, project):
    badge, created = Badge.objects.get_or_create(name=f"Completed {project.name}")
    badge.users.add(user)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from django.views import View
from .forms import ProjectForm


def projects(request):
    projectsList = Project.objects.all()
    context = {'projects': projectsList}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/single_project.html', {'project': projectObj})


class CreateProject(View):
    form_class = ProjectForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'projects/project_form.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')


class UpdateProject(View):
    form_class = ProjectForm

    def setup(self, request, *args, **kwargs):
        self.project_instance = get_object_or_404(Project, pk = kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, pk):
        project = self.project_instance
        form = self.form_class(instance=project)
        return render(request, 'projects/project_form.html', {'form': form})

    def post(self, request, pk):
        project = self.project_instance
        form = self.form_class(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')


class DeleteProject(View):
    form_class = ProjectForm

    def setup(self, request, *args, **kwargs):
        self.project_instance = get_object_or_404(Project, pk = kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, pk):
        obj = self.project_instance
        return render(request, 'projects/delete_template.html', {'obj': obj})

    def post(self, request, pk):
        project = self.project_instance
        project.delete()
        return redirect('projects')
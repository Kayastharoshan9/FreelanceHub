from django.shortcuts import render
from django.http import HttpResponse
from .models import Project


def projects(request):
    projectsList = Project.objects.all()
    context = {'projects': projectsList}
    return render(request, 'projects/list.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/single.html', {'project': projectObj})
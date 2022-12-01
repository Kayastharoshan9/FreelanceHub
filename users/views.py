from django.shortcuts import render
from django.views import View
from .models import Profile


class ProfileListView(View):
    def get(self, request):
        profiles = Profile.objects.all()
        context = {'profiles': profiles}
        return render(request, 'users/profiles.html', context)
from django.shortcuts import render
from django.views import View
from .models import Profile


class ProfileListView(View):
    def get(self, request):
        profiles = Profile.objects.all()
        context = {'profiles': profiles}
        return render(request, 'users/profiles.html', context)


class ProfileDetailView(View):
    def get(self, request, pk):
        profile = Profile.objects.get(id=pk)
        topSkills = profile.skill_set.exclude(description__exact="")
        otherSkills = profile.skill_set.filter(description="")
        context = {'profile': profile, 'topSkills': topSkills,
               "otherSkills": otherSkills}
        return render(request, 'users/profile_detail.html', context)
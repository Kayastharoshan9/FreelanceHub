from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginUserView(View):
    page = 'login'
    def get(self, request):
        context = {'page': self.page}
        return render(request, 'users/login_register.html', context)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username OR password is incorrect')
        return render(request, 'users/login_register.html', {'page': self.page})


class LogoutUserView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, 'User was logged out!')
        return redirect('login')


class RegisterUserView(View):
    page = 'register'
    form = CustomUserCreationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'page': self.page, 'form': self.form}
        return render(request, 'users/login_register.html', context)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'An error has occurred during registration')
        return render(request, 'users/login_register.html', {'page': self.page, 'form': form})


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


class UserAccountView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        skills = profile.skill_set.all()
        projects = profile.project_set.all()
        context = {'profile': profile, 'skills': skills, 'projects': projects}
        return render(request, 'users/account.html', context)


class EditAccountView(LoginRequiredMixin, View):
    form = ProfileForm

    def setup(self, request, *args, **kwargs):
        self.profile_instance = request.user.profile
        return super().setup(self, request, *args, **kwargs)

    def get(self, request):
        form = self.form(instance=self.profile_instance)
        context = {'form': form}
        return render(request, 'users/profile_form.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile_instance)
        if form.is_valid():
            form.save()
            return redirect('account')
        return render(request, 'users/profile_form.html', {'form': form})
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name="login"),
    path('logout/', views.LogoutUserView.as_view(), name="logout"),
    path('register/', views.RegisterUserView.as_view(), name="register"),
    
    path('', views.ProfileListView.as_view(), name="profiles"),
    path('profile/<str:pk>/', views.ProfileDetailView.as_view(), name="profile-detail"),
    path('account/', views.UserAccountView.as_view(), name="account"),
]
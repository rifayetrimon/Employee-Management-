from . import views
from django.urls import path


urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_view, name='login'),
    path('home', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout_view, name='logout'),
    path('create_event', views.create_event, name='create_event'),
    path('create_category', views.create_category, name='create_category'),
]

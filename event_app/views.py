from django.contrib import messages
from django.shortcuts import render, redirect
from . forms import CustomAuthenticationForm, CustomUserCreationForm, EventForm,EventCategoryForm
from django.contrib.auth import login, authenticate, logout
from .models import Event, EventCategory
# Create your views here.



# register user 
def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)    
            messages.success(request, f'Your account has been created! You are now able to log in')    
        else:
            messages.error(request, f'Invalid data! Please check the data')

    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/registration.html', {'form': form})


# login user 

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=user_name, password=password)
            if user is not None:

                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


def home(request):
    events = Event.objects.all()
    
    return render(request, 'home.html', {'events': events})


def profile(request):
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
        else:
            messages.error(request, 'Invalid data! Please check the data')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


def create_category(request):
    if request.method == "POST":
        form = EventCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event Category created successfully!')
        else:
            messages.error(request, 'Invalid data! Please check the data')
    else:
        form = EventCategoryForm()
    return render(request, 'create_category.html', {'form': form})



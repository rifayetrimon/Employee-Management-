from unicodedata import category
from django.contrib import messages
from django.shortcuts import render, redirect
from . forms import CustomAuthenticationForm, CustomUserCreationForm, EditProfileForm, EventForm,EventCategoryForm
from django.contrib.auth import login, authenticate, logout
from .models import Event, EventCategory, Booking, Profile
from django.db.models import Q
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
    user = request.user
    search = request.GET.get('search')
    category_id = request.GET.get('category')

    events = Event.objects.all()

    if search:
        events = events.filter(
            Q(name__icontains=search) |
            Q(date__icontains=search) |
            Q(location__icontains=search)
        )


    if category_id:
        events = events.filter(category_id=category_id)


    events_with_status = []

    for event in events:
        is_booked = Booking.objects.filter(user=user, event=event).exists()
        events_with_status.append({
            'event': event,
            'is_booked': is_booked
        })
    categories = EventCategory.objects.all()
    
    return render(request, 'home.html', {'events': events_with_status, 'user': user, 'categories': categories})



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



def my_events(request):
    if request.user.username == 'admin':
        events = Event.objects.all()
    else:
        events = Event.objects.filter(created_by=request.user)

    return render(request, 'my_events.html', {'events': events})



def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.user != event.created_by and request.user.username != 'admin':
        messages.error(request, 'You are not authorized to edit this event!')
        return redirect('my_events')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('my_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'edit_event.html', {'form': form})



def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.user == event.created_by or request.user.username == 'admin':   
        event.delete()
        messages.success(request, 'Event deleted successfully!')
    else:
        messages.error(request, 'You are not authorized to delete this event!')

    return redirect('my_events')



def book_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if Booking.objects.filter(user=request.user, event=event).exists():
        messages.error(request, 'You have already booked this event!')
        return redirect('home')

    if event.capacity > 0:
        event.capacity -= 1
        event.save()
        booking = Booking.objects.create(user=request.user, event=event)
        messages.success(request, 'Event booked successfully!')
    else:
        messages.error(request, 'Event is fully booked!')
    return redirect('booked_events')



def booked_events(request):
    bookings = Booking.objects.filter(user=request.user).select_related('event')
    return render(request, 'booked_event.html', {'bookings': bookings})


def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    event = booking.event
    event.capacity += 1
    event.save()
    booking.delete()
    return redirect('booked_events')




def edit_profile(request):
    profile_instance = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user, profile_instance=profile_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
    else:
        form = EditProfileForm(instance=request.user, profile_instance=profile_instance)
    return render(request, 'edit_profile.html', {'form': form})

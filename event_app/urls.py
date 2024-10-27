from . import views
from django.urls import path


urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout_view, name='logout'),
    path('create_event', views.create_event, name='create_event'),
    path('create_category', views.create_category, name='create_category'),
    path('my_events', views.my_events, name='my_events'),
    path('delete_event/<int:event_id>', views.delete_event, name='delete_event'),
    path('edit_event/<int:event_id>', views.edit_event, name='edit_event'),
    path('book_event/<int:event_id>', views.book_event, name='book_event'),
    path('my_bookings/', views.booked_events, name='booked_events'),
    path('cancel_booking/<int:booking_id>', views.cancel_booking, name='cancel_booking'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

]

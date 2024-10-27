from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from . models import Profile, Event


class CustomUserCreationForm(UserCreationForm):

    contact = forms.CharField(max_length=15, required=True, help_text="Enter your contact number")
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-input mt-2 block w-full bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-base py-2 px-3',
            'placeholder': 'Username'
        })
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-input mt-2 block w-full bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-base py-2 px-3',
            'placeholder': 'Email'
        })
        self.fields['contact'].widget = forms.TextInput(attrs={
            'class': 'form-input mt-2 block w-full bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-base py-2 px-3',
            'placeholder': 'Contact Number'
        })

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

        Profile.objects.create(user=user, contact=self.cleaned_data['contact'])

        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input mt-2 block w-full bg-white border border-gray-300 rounded-lg py-2 px-3',
        'placeholder': 'Enter your username',
        'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input mt-2 block w-full bg-white border border-gray-300 rounded-lg py-2 px-3',
        'placeholder': 'Enter your password',
    }))




class EditProfileForm(forms.ModelForm):
    contact = forms.CharField(
        max_length=15,
        required=True,
        help_text="Enter your contact number"
    )

    class Meta:
        model = User
        fields = ('username', 'email')  

    def __init__(self, *args, **kwargs):
        profile_instance = kwargs.pop('profile_instance', None)  
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-input mt-2 block w-full bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-base py-2 px-3',
            'placeholder': 'Username'
        })
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-input mt-2 block w-full bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-base py-2 px-3',
            'placeholder': 'Email'
        })

        if profile_instance:
            self.fields['contact'].initial = profile_instance.contact
        self.fields['contact'].widget = forms.TextInput(attrs={
            'class': 'form-input mt-2 block w-full bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-base py-2 px-3',
            'placeholder': 'Contact Number'
        })

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=commit)
        if commit:
            profile = Profile.objects.get(user=user)
            profile.contact = self.cleaned_data['contact']
            profile.save()
        return user





class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'location', 'capacity', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input mt-1 p-3 block w-full', 'placeholder': 'Event Name', }),
            'description': forms.Textarea(attrs={'class': 'form-textarea mt-1 p-3 block w-full', 'placeholder': 'Event Description', 'rows': 4}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input mt-1 p-3 block w-full'}),
            'location': forms.TextInput(attrs={'class': 'form-input mt-1 p-3 block w-full', 'placeholder': 'Location'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-input mt-1 p-3 block w-full', 'placeholder': 'Capacity'}),
            'category': forms.Select(attrs={'class': 'form-select mt-1 p-3 block w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] += ' border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500'



from django import forms
from .models import EventCategory

class EventCategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input mt-1 p-3 block w-full', 'placeholder': 'Category Name', }),
            'description': forms.Textarea(attrs={'class': 'form-textarea mt-1 p-3 block w-full', 'placeholder': 'Category Description', 'rows': 4})
        }
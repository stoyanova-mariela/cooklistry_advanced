from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    email = forms.EmailField(
        required=True,
        label='Email address',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email already registered.')
        return email

    def save(self, commit=True):
        email = self.cleaned_data.get('email')
        user = super().save(commit=False)
        user.email = email

        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password',
        })


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'favourite_cuisine']

        labels = {
            'bio': 'About Me',
            'profile_picture': 'Profile Picture',
            'favourite_cuisine': 'Favourite Cuisine',
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us something about yourself...',
                'rows': 4,
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'favourite_cuisine': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Italian, Bulgarian, Japanese',
            }),
        }

    def clean_favourite_cuisine(self):
        cuisine = self.cleaned_data['favourite_cuisine'].strip()

        if cuisine and len(cuisine) < 3:
            raise forms.ValidationError('Favourite cuisine must contain at least 3 characters.')

        return cuisine
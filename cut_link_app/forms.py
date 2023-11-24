from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import ShortenedUrl


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Add a valid e-mail address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email address already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UrlSubmitForm(forms.ModelForm):
    class Meta:
        model = ShortenedUrl
        fields = ['original_url']
        labels = {
            'original_url': 'Enter URL to shorten'
        }
        widgets = {
            'original_url': forms.URLInput(attrs={'class': 'form-control'})
        }

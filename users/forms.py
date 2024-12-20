from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from menu.models import RestaurantMenu, Restaurant, Order, Category, Review


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput,
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'cost', 'category', 'picture']
        widgets = {
            'picture': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        }


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone_number', 'picture']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rate', 'description']

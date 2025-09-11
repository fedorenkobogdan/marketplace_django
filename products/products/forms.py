from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Product, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, label="Ім'я")

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")

class UserUpdateForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ("username", "first_name", "email")
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CheckoutForm(forms.Form):
    full_name = forms.CharField(label="Ім'я та прізвище", max_length=100)
    address = forms.CharField(label="Адреса доставки", widget=forms.Textarea)
    phone = forms.CharField(label="Телефон", max_length=20)










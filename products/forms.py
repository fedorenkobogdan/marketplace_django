from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Product, Comment

# 🔐 Реєстрація користувача
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, label="Ім'я")

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")


# 🧑‍💼 Оновлення профілю
class UserUpdateForm(UserChangeForm):
    password = None  # щоб не показувалося поле паролю

    class Meta:
        model = User
        fields = ("username", "first_name", "email")


# 📦 Форма товару
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']


# 💬 Форма коментаря
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="Ваш коментар",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Напишіть коментар тут...",
            "rows": 3
        })
    )

    class Meta:
        model = Comment
        fields = ['content']


# ✅ Оформлення замовлення
class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        label="Ім'я та прізвище", 
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    address = forms.CharField(
        label="Адреса доставки",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3})
    )
    phone = forms.CharField(
        label="Телефон", 
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )










from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(label="Имя", max_length=120)
    phone = forms.CharField(label="Телефон", max_length=40)
    address = forms.CharField(label="Адрес", max_length=300)
    qty = forms.IntegerField(label="Количество", min_value=1, initial=1)

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']



class ShippingAddressForm(forms.Form):
    address = forms.CharField(max_length=128)
    apartment_number = forms.CharField(max_length=128)
    city = forms.CharField(max_length=128)
    state = forms.CharField(max_length=128)
    postal_code = forms.CharField(max_length=128)
    phone_number = forms.CharField(max_length=128)

from django import forms
from django.forms import CharField, Form, PasswordInput



class ContactForm(forms.Form):
    """
    Registration form
    """

    first_name = forms.CharField(label="First name", max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(label="Last name", max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
    email = forms.CharField(label="Email", max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "name@example.com"}))
    message = forms.CharField(label="Message", required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter a message here!"}))




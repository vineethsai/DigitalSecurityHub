from django import forms
from django.forms import CharField, Form, PasswordInput



class ContactForm(forms.Form):
    """
    Registration form
    """

    first_name = forms.CharField(label='First name', max_length=30, required=True)
    last_name = forms.CharField(label='Last name', max_length=30, required=True)
    email = forms.CharField(label='Email', max_length=30, required=True)
    message = forms.CharField(label='Message', required=True)




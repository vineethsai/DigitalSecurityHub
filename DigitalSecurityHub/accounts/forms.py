from django import forms
from django.forms import CharField, Form, PasswordInput
from django.utils.translation import ugettext_lazy as _


RELEVANCE_CHOICES = (
        (0, _("Customer")),
        (1, _("Vendor"))
    )


class SignupForm(forms.Form):
    """
    Registration form
    """

    first_name = forms.CharField(label='First name', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last name', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=30, required=True,
                               widget=PasswordInput(attrs={'class': 'form-control'}))
    password_conf = forms.CharField(label='Password Confirmation', max_length=30, required=True,
                                    widget=PasswordInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(choices=RELEVANCE_CHOICES, widget=forms.RadioSelect, required=True)


class SigninForm(forms.Form):
    """
    Signin form
    """
    username = forms.CharField(label='Username', max_length=30, required=True,  widget=forms.TextInput(attrs={'placeholder': 'Username or Email', 'class': 'form-control'}))
    password = forms.CharField(label='password', max_length=30, required=True, widget=PasswordInput(attrs={'placeholder': '*******', 'class': 'form-control'}))


class CustomerForm(forms.Form):
    """
    Registration form
    """
    address = forms.CharField(label='Address', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label='City', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(label='State', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip = forms.IntegerField(label='Zip code', required=True)
    # birth_date = forms.DateField(label='Birth Date', required=True, widget=forms.SelectDateWidget())


class CompanyForm(forms.Form):
    name = forms.CharField(label='Company Name', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Company Address', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label='City', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(label='State', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip = forms.IntegerField(label='Zip code', required=True)


class DeleteForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30, required=True)

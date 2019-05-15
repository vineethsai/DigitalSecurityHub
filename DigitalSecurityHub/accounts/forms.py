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

    first_name = forms.CharField(label='First name', max_length=30, required=True)
    last_name = forms.CharField(label='Last name', max_length=30, required=True)
    email = forms.CharField(label='Email', max_length=30, required=True)
    username = forms.CharField(label='Username', max_length=30, required=True)
    password = forms.CharField(label='Password', max_length=30, required=True,
                               widget=PasswordInput())
    password_conf = forms.CharField(label='Password Confirmation', max_length=30, required=True,
                                    widget=PasswordInput())
    type = forms.ChoiceField(choices=RELEVANCE_CHOICES, widget=forms.RadioSelect, required=True)


class SigninForm(forms.Form):
    """
    Signin form
    """
    username = forms.CharField(label='Username', max_length=30, required=True)
    password = forms.CharField(label='password', max_length=30, required=True, widget=PasswordInput())


class CustomerForm(forms.Form):
    """
    Registration form
    """
    address = forms.CharField(label='Address', widget=forms.Textarea, required=True)
    city = forms.CharField(label='City', max_length=30, required=True)
    state = forms.CharField(label='State', max_length=30, required=True)
    zip = forms.IntegerField(label='Zip code', required=True)
    # birth_date = forms.DateField(label='Birth Date', required=True, widget=forms.SelectDateWidget())


class CompanyForm(forms.Form):
    name = forms.CharField(label='Company Name', max_length=30, required=True)
    address = forms.CharField(label='Company Address', max_length=30, required=True)
    city = forms.CharField(label='City', max_length=30, required=True)
    state = forms.CharField(label='State', max_length=30, required=True)
    zip = forms.IntegerField(label='Zip code', required=True)


class DeleteForm(forms.Form):
    name = forms.CharField(label='Company Name', max_length=30, required=True)

from django import forms
from django.forms import CharField, Form 

from django.utils.translation import ugettext_lazy as _


RELEVANCE_CHOICES = (
        (_("True"), True),
        (_("False"), False)
    )

class ProductCreationForm(forms.Form):
    """
    Registration form
    """

    title = forms.CharField(label='Title', max_length=120, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}))
    description = forms.CharField(label='Description', max_length=1500, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    active = forms.ChoiceField(choices=RELEVANCE_CHOICES, widget=forms.RadioSelect, required=True)
    category = forms.CharField(label='Category', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a category here!'}))
    price = forms.IntegerField(label='Price', required= True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '100'}))
    stock = forms.IntegerField(label='Stock', required= True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5'}))


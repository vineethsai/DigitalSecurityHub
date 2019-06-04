from django import forms
from django.forms import CharField, Form



class CheckoutForm(forms.Form):
    """
    Checkout form
    """

    first_name = forms.CharField(label="First name", max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last name", max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(label="City", max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    state = forms.CharField(label="State", max_length=4, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    zip = forms.IntegerField(label="Zip code", required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
    card_name = forms.CharField(label="Name on card", max_length=60, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    cred_card_number = forms.IntegerField(label="Card number", required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
    expiration = forms.CharField(label="Expiration", max_length=5, required=True, widget=forms.DateInput(format="%m/%d  ",attrs={"class": "form-control"}))
    cvv = forms.IntegerField(label="CVV", required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))

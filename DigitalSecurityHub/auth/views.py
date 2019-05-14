from django.shortcuts import render
from django.forms.models import model_to_dict
from products.views import output_company

# Create your views here.
def output_user(user):
    """
    Returns output dict for user
    """
    return model_to_dict(user, fields=["id", "username", "first_name", "last_name", "email"])

def output_customer(customer):
    """
    Returns output dict for customer
    """
    return {
        "User": output_user(customer.user),
        "BirthDate": customer.birth_date,
        "Address": customer.address,
        "City": customer.city,
        "State": customer.state,
        "Zip": customer.zip
    }

def output_seller(seller):
    """
    Returns output dict for seller
    """
    return {
        "User": output_user(seller.user),
        "Company": output_company(seller.company)
    }

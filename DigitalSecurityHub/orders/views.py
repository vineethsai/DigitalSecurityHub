from django.shortcuts import render
from accounts.models import Customer
from accounts.views import output_customer

# Create your views here.
def output_order(order):
    return {
        "Customer": output_customer(order.customer_id),
        "OrderDate": order.order_date,
        "Total": order.order_total
    }
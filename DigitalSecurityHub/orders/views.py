from django.shortcuts import render
from accounts.models import Customer
from accounts.views import output_customer
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Order

# Create your views here.
def output_order(order):
    return {
        "Customer": output_customer(order.customer_id),
        "OrderDate": order.order_date,
        "Total": order.order_total
    }

def specificOrder(request, order_id):
    
    if request.method is 'GET':
        order = Order.objects.get(id=order_id)
        return JsonResponse(order, safe=False)

    if request.method is 'PATCH':
        pass

    if request.method is 'DELETE':
        pass
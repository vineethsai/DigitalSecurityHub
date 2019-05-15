from django.shortcuts import render
from accounts.models import Customer
from accounts.views import output_customer
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Order
from django.db.models import Q
import json


# Create your views here.
def output_order(order):
    return {
        "Customer": output_customer(order.customer_id),
        "OrderDate": order.order_date,
        "Total": order.order_total
    }

def specificOrder(request, order_id):
    """
    GET: lists information about specific order
    DELETE: cancel order
    PATCH: change order details
    """
    # Get the specified order information for logged in user and return in json if it exists
    if request.method == 'GET' and request.user.is_authenticated:
        try:
            order = output_order(Order.objects.get(Q(id=order_id) & Q(customer_id=request.user)))  # <-- i think that customer_id needs to have _id or _pk added to it to let it know is needs to join tables based on that
            return JsonResponse(order, safe=False)
        except:
            return HttpResponse('Order not found', status=500)
    else:
        return HttpResponse("Not authorized", status=401)

    # Allows logged in user to update order
    if request.method == 'PATCH' and request.user.is_authenticated:
        try:
            json_post = json.loads(request.body)
            order = Order.objects.get(Q(id=order_id) & Q(customer_id=request.user))  # <-- get specified order for currently logged in user
            order.order_date = json_post['order_date']
            order.save()
            return HttpResponse('Order has been updated')
        except:
            return HttpResponse('Order does not exist', status=500)
    else:
        return HttpResponse("Not authorized", status=401)

    # Allows current logged in user to cancel order
    if request.method == 'DELETE' and request.user.is_authenticated:
        try:
            Order.objects.get(Q(id=order_id) & Q(customer_id=request.user)).delete()
            return HttpResponse('Order has been deleted')
        except:
            return HttpResponse('The order could not be deleted', status=500)
    else:
        return HttpResponse("Not authorized", status=401)

    return HttpResponse('Method not allowed', status=405)

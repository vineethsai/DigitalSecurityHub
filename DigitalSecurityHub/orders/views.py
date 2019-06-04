from django.shortcuts import render
from accounts.models import Customer
from cart.models import Cart
from accounts.views import output_customer
from products.views import output_product
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, LineItem
from django.db.models import Q
from orders.forms import CheckoutForm
import json


# Create your views here.
def output_order(order, sensitive=False):
    return_obj = {
        "Customer": output_customer(order.customer_id),
        "OrderDate": order.order_date,
        "Total": order.order_total,
        "ShippingName": order.shipping_name,
        "ShippingAddress": order.shipping_address,
        "ShippingCity": order.shipping_city,
        "ShippingState": order.shipping_state,
        "ShippingZIP": order.shipping_zip
    }

    if sensitive:
        return_obj["BillingName"] = billing_name
        return_obj["BillingCard"] = billing_card
        return_obj["BillingExpiration"] = billing_expiration
        return_obj["BillingCVV"] = billing_cvv

    return return_obj

def output_line_item(lineItem):
    return {
        "Order": output_order(lineItem.order_id),
        "Product": output_product(lineItem.product_id),
        "Quantity": lineItem.quantity,
        "Price": lineItem.price_extended
    }

def order(request):
    """
    GET: renders all the users previous orders.
    """
    if not request.user.is_authenticated:
        return render(request, "error.html", {
            "errorcode": 401,
            "message": "Looks like you don't have permission to view this content!",
        }, status=401)

    # Attempts to get all user orders
    try:
        customer = Customer.objects.get(customer_id=request.user)
    except:
        return render(request, "error.html", {
            "errorcode": 404,
            "message": "Oops! This user could not be found!",
            "message2": "Sorry but the user you are looking for does not exist or has been removed."
        }, status=404)
    try:
        orders = Order.objects.filter(customer_id=customer)
    except:
        return render(request, "error.html", {
            "errorcode": 404,
            "message": "Oops! Orders could not be found!",
            "message2": "Sorry but the orders you are looking for does not exist or has been removed."
        }, status=404)

    if request.method == "GET":
        order_list = []
        for order in orders:
            formatted_order = output_order(order)
            formatted_order["uid"] = order.id


            # Attempts to get all line items
            try:
                line_item_list = []
                line_items = LineItem.objects.filter(order_id=order)

                for line_item in line_items:
                    line_item_list.append(output_line_item(line_item))
                formatted_order["lineItems"] = line_item_list
            except:
                return render(request, "error.html", {
                    "errorcode": 404,
                    "message": "Oops! Not all line items could not be found!",
                    "message2": "Sorry but the orders you are looking for is having issues right now."
                }, status=404)
            order_list.append(formatted_order)

        return render(request, "orders/orders.html", {
            "orders": order_list
        })


    return HttpResponse("Method not allowed", status=405)

def checkout(request):
    """
    GET: renders the checkout page.
    """
    from cart.views import output_cart

    if not request.user.is_authenticated:
        return render(request, "error.html", {
            "errorcode": 401,
            "message": "Looks like you don't have permission to view this content!",
        }, status=401)

    # Attempts to get users all items in users cart
    try:
        customer = Customer.objects.get(customer_id=request.user)
    except:
        return render(request, "error.html", {
            "errorcode": 404,
            "message": "Oops! This user could not be found!",
            "message2": "Sorry but the user you are looking for does not exist or has been removed."
        }, status=404)

    try:
        cart = Cart.objects.filter(customer_id=customer)
    except:
        return render(request, "error.html", {
            "errorcode": 404,
            "message": "Oops! This cart could not be found!",
            "message2": "Sorry but the cart you are looking for does not exist or has been removed."
        }, status=404)

    if request.method == "GET":
        cart_list = []
        total_cost = 0


        # Compiles list of all items in cart
        for item in cart:
            output_base = output_cart(item)
            output_base["product_id"] = item.product_id.id
            cart_list.append(output_base)
            total_cost += item.quantity * item.product_id.price

        # Renders the checkout page
        form = CheckoutForm()
        return render(request, "orders/checkout.html", {
            "cart_items": cart_list,
            "total": total_cost,
            "form": form
        })

    return HttpResponse("Method not allowed", status=405)

@csrf_exempt
def specificOrder(request, order_id):
    """
    GET: lists information about specific order
    DELETE: cancel order
    PATCH: change order details
    """
    # Get the specified order information for logged in user and return in json if it exists
    if request.method == "GET" and request.user.is_authenticated:
        try:
            order = output_order(Order.objects.get(Q(id=order_id) & Q(customer_id=Customer.objects.get(customer_id=request.user))))  # <-- i think that customer_id needs to have _id or _pk added to it to let it know is needs to join tables based on that
            return JsonResponse(order, safe=False)
        except:
            return render(request, "error.html", {
                "errorcode": 404,
                "message": "Oops! This order could not be found!",
                "message2": "Sorry but the order you are looking for does not exist or has been removed."
            }, status=404)

    # Allows logged in user to update order
    if request.method == "PATCH" and request.user.is_authenticated:
        try:
            json_post = json.loads(request.body)
            order = Order.objects.get(Q(id=order_id) & Q(customer_id=Customer.objects.get(customer_id=request.user)))  # <-- get specified order for currently logged in user
            order.order_date = json_post["order_date"]
            order.save()
            return HttpResponse("Order has been updated")
        except:
            return HttpResponse("Order does not exist", status=500)

    # Allows current logged in user to cancel order
    if request.method == "DELETE" and request.user.is_authenticated:
        try:
            Order.objects.get(Q(id=order_id) & Q(customer_id=Customer.objects.get(customer_id=request.user))).delete()
            return HttpResponse("Order has been deleted")
        except:
            return HttpResponse("The order could not be deleted", status=500)
    else:
        return HttpResponse("Not authorized", status=401)

    return HttpResponse("Method not allowed", status=405)

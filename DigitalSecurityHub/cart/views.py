import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from cart.models import Cart
from orders.models import Order, LineItem
from orders.view import output_order
from auth.models import Customer
from products.models import Product

# Create your views here.
def cart(request):
    """
    Allows user to interact with their cart
    GET: shows cart
    POST: submits cart to order
    DELETE: removes item from cart - JSON input should include item
        OPTIONAL: delete quantity
    """
    # Verifies user is signed in.
    if request.user.is_authenticated:
        return HttpResponse(status=401)

    # Attempts to get users all items in users cart
    try:
        cart = Cart.objects.filter(customer_id=request.user.id)
    except:
        return HttpResponse("Failed to find users cart.", status=404)

    if request.method == "GET":
        cart_list = []

        # Compiles list of all items in cart
        for item in cart:
            cart_list.append(output_cart(item))

        # Returns json serialized message
        return JsonResponse(user_list, safe=False)

    if request.method == "POST":
        # Adds up cart total
        total = 0
        for item in cart:
            total += item.product_id.price * item.quantity

        # Creates new order
        try:
            new_order = Order.objects.create(
                customer_id = Customer.objects.get(id=request.user.id),
                order_total = total
            )
        except:
            return HttpResponse("Failed to create order", status=500)

        # Adds each item in cart to line item
        for item in cart:
            try:
                LineItem.objects.create(
                    order_id = new_order,
                    product_id = Product.objects.get(id=item.product_id.id),
                    quantity = item.quantity,
                    price_extended = item.product_id.price * item.quantity
                )
            except:
                return HttpResponse("Failed to create all line items. Order still processed", status=500)

            return JsonResponse(output_order(new_order), safe=False)


    return HttpResponse("Method not allowed on shop/" + product_id, status=405)



def output_cart(cart):
    """
    Returns cart dict
    """
    return {
        "Customer": output_customer(cart.customer_id),
        "Product": output_product(cart.product_id),
        "Quantity": cart.quantity
    }
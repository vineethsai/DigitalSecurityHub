import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from cart.models import Cart
from orders.models import Order, LineItem
from orders.views import output_order
from accounts.models import Customer
from accounts.views import output_customer
from products.models import Product
from products.views import output_product


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
    # if request.user.is_authenticated:
        # return HttpResponse(status=401)

    # Attempts to get users all items in users cart
    try:
        cart = Cart.objects.filter(customer_id=request.user.customer)
    except:
        return HttpResponse("Failed to find users cart.", status=404)

    if request.method == "GET":
        cart_list = []

        # Compiles list of all items in cart
        for item in cart:
            cart_list.append(output_cart(item))

        # Returns json serialized message
        return JsonResponse(cart_list, safe=False)

    if request.method == "POST":
        # Adds up cart total
        total = 0
        for item in cart:
            total += item.product_id.price * item.quantity

        # Creates new order
        try:
            new_order = Order.objects.create(
                customer_id = Customer.objects.get(user=request.user),
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

    if request.method == "DELETE":
        # Attempt to get JSON
        try:
            json_post = json.loads(request.body)
        except:
            return HttpResponse("Failed to process json.", status=500)

        # Attempts to get item in cart
        try:
            product = Product.objects.get(id=json_post["product_id"])
            item_to_delete = cart.filter(product_id=product)
        except:
            return HttpResponse("Failed to find that item.", status=404)

        # Checks if there are any items to delete
        if len(item_to_delete) is 0:
            return HttpResponse("Failed to find that item.", status=404)

        # Deletes any item even if there are duplicate entries
        for item in item_to_delete:
            try:
                if "quantity" in json_post:
                    if (item.quantity - int(json_post["quantity"]) <= 0):
                        item.delete()
                    else:
                        item.quantity -= int(json_post["quantity"])
                        item.save
                else:
                    item.delete()
            except:
                return HttpResponse("Failed to delete item.", status=500)

            return HttpResponse("Item deleted!", status=200)

    # No other HTTP methods allowed
    return HttpResponse("Method not allowed on shop/", status=405)



def output_cart(cart):
    """
    Returns cart dict
    """
    return {
        "Customer": output_customer(cart.customer_id),
        "Product": output_product(cart.product_id),
        "Quantity": cart.quantity
    }
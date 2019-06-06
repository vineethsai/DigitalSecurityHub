import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from cart.models import Cart
from orders.models import Order, LineItem
from orders.views import output_order
from orders.forms import CheckoutForm
from accounts.models import Customer
from accounts.views import output_customer
from products.models import Product
from products.views import output_product
from django.views.decorators.debug import sensitive_post_parameters




# Create your views here.
@sensitive_post_parameters()
def cart(request):
    """
    Allows user to interact with their cart
    GET: shows cart
    POST: submits cart to order
    DELETE: removes item from cart - JSON input should include item
        OPTIONAL: delete quantity
    """
    # Verifies user is signed in.
    if not request.user.is_authenticated:
        return render(request, "error.html", {
            "errorcode": 401,
            "message": "Not authorized!",
            "message2": "Looks like you don't have permission to view this content."
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

        # Returns json serialized message
        return render(request, "cart/cart.html", {
            "cart_items": cart_list,
            "total": total_cost
        })

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if not form.is_valid():
            return render(request, "error.html", {
                "errorcode": 500,
                "message": "Failed to create order!",
                "message2": "Try redoing your checkout."
            }, status=500)

        # Adds up cart total
        total = 0
        for item in cart:
            total += item.product_id.price * item.quantity

        # Creates new order
        try:
            new_order = Order.objects.create(
                customer_id = Customer.objects.get(customer_id=request.user),
                order_total = total,
                shipping_name = form.cleaned_data["first_name"] + " " + form.cleaned_data["last_name"],
                shipping_address = form.cleaned_data["address"],
                shipping_city = form.cleaned_data["city"],
                shipping_state = form.cleaned_data["state"],
                shipping_zip = form.cleaned_data["zip"],
                billing_name = form.cleaned_data["card_name"],
                billing_card = form.cleaned_data["cred_card_number"] % 100000,
                billing_expiration = form.cleaned_data["expiration"],
                billing_cvv = form.cleaned_data["cvv"],
            )
        except:
            return render(request, "error.html", {
                "errorcode": 500,
                "message": "Failed to create order!",
                "message2": "Try redoing your checkout."
            }, status=500)

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
                return render(request, "error.html", {
                    "errorcode": 500,
                    "message": "Failed to create all line items! Order still processed!",
                    "message2": "Some items will have to be added later."
                }, status=500)

        # Clears cart
        for item in cart:
            try:
                item.delete()
            except:
                pass # Can be easily spotted and resolved by users later

            return HttpResponseRedirect("/orders")

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
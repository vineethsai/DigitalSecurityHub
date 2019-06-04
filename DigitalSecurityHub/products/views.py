from django.shortcuts import render
from django.views.generic import ListView
from accounts.views import output_seller
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from cart.models import Cart
from shop.models import Review
from accounts.models import Customer, Seller, Company, User
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import ProductCreationForm

from .models import Product

@csrf_exempt
def ProductList(request):
    """
    GET: renders JSON of all products
    POST: adds a new product
    DELETE: deletes all products owned by this user
    """
    products = Product.objects.all()

    # Returns a list of all current products
    if request.method == "GET":
        # render a list of all the product titles
        return render(request, "products/productList.html", {"object_list": Product.objects.all(),
        "Seller": Seller,
        "Company": Company}, status=200)

    # Allows a vendor to add a new product
    if request.method == "POST" and request.user.is_authenticated and Seller.objects.get(seller_id=request.user):
        try:
            form = ProductCreationForm(request.POST)
            if form.is_valid():
                Product.objects.create(
                    title = form.cleaned_data["title"],
                    description = form.cleaned_data["description"],
                    price = form.cleaned_data["price"],
                    stock = form.cleaned_data["stock"],
                    active = form.cleaned_data["active"],
                    category = form.cleaned_data["category"],
                    seller_id = Seller.objects.get(seller_id=request.user),
                )
                return HttpResponseRedirect("/shop/")
        except:
            return HttpResponse("Failed to add new product.", status=500)

    # Allows the current user to delete all products owned by them
    if request.method == "DELETE" and request.user.is_authenticated and Seller.objects.get(seller_id=request.user):
        try:
            seller = Seller.objects.get(seller_id=request.user)
            product_list = Product.objects.filter(seller_id=seller).delete()
            return HttpResponseRedirect("/shop/")
        except:
            return HttpResponse("Failed to delete products.", status=500)

    # Returns if user is not authenticated
    if not request.user.is_authenticated:
        return HttpResponse("Not authorized", status=401)

    # Return 405 if any other method besides the ones specified above is tried
    return HttpResponse("Method not allowed", status=405)

@csrf_exempt
def SpecificProduct(request, product_id):
    """
    GET: renders JSON of specific product
    POST: adds product to cart
    PATCH: edits product information if seller
    DELETE: deletes product if seller
    """
    # Import done here to allow prior dependencies to compile
    from shop.views import output_review

    # Returns product information for the specified product
    if request.method == "GET":
        # Try to get all reviews
        try:
            reviews = []
            rating_sum = 0
            rating_count = 0
            for review in Review.objects.filter(product_id=product_id):
                reviews.append(output_review(review))
                rating_sum += review.rating
                rating_count += 1
        except:
            return HttpResponse("Failed to get all reviews", status=500)

        # Attempts to get product
        try:
            product_obj = Product.objects.get(id=product_id)
        except:
            return HttpResponse("Could not find product", status=404)

        # Checks if user is the seller
        is_seller = 0
        try:
            seller = Seller.objects.get(seller_id=request.user)
            print(product_obj)
            print(seller)
            is_seller = 0 if seller is product_obj.seller_id else 1
        except:
            pass # if this fails it could just mean they aren't a seller so we don't care

        # Renders the page
        try:
            product = output_product(product_obj)
            return render(request, "products/product.html", {
                "product": product,
                "reviews":reviews,
                "avg_rating": 0 if rating_count is 0 else round(rating_sum / rating_count, 1),
                "product_id": product_id,
                "company": Seller.objects.get(seller_id=Product.objects.get(id=product_id).seller_id).company_id.name,
                "isSeller": is_seller
            })
        except:
            return HttpResponse("Request failed", status=500)

    # Should add the product to the cart of the authenticated user
    if request.method == "POST" and request.user.is_authenticated:
        try:
            json_post = None
            if request.body:
                json_post = json.loads(request.body)

            # Determines if quantity is default or not
            quantity = 1
            if json_post is not None and json_post["quantity"]:
                quantity = json_post["quantity"]

            # Creates new cart object
            Cart.objects.update_or_create(customer_id=Customer.objects.get(customer_id=request.user),
                                        product_id=Product.objects.get(id=product_id),
                                        defaults={"quantity": quantity})
            return HttpResponse("Product added")  # <-- product should be added to the current logged in user"s cart
        except:
            return HttpResponse("Could not add product to cart.", status=500)

    # Allows seller to edit product information (if it is their product)
    if request.method == "PATCH" and request.user.is_authenticated and Customer.objects.get(customer_id=request.user).type:
        try:
            json_post = json.loads(request.body)
            product = Product.objects.get(Q(id=product_id) & Q(seller_id=Seller.objects.get(seller_id=request.user)))  # <-- should get the specified product of the current logged in seller
            product.title = json_post["title"]
            product.description = json_post["description"]
            product.price = json_post["price"]
            # product.seller = json_post["seller"]
            product.stock = json_post["stock"]
            product.active = json_post["active"]
            product.save()
            return HttpResponse("Product updated")
        except:
            return HttpResponse("Product could not be updated")

    # Will delete the specified product if owned by the current seller
    if request.method == "DELETE" and request.user.is_authenticated:
        try:
            product = Product.objects.get(id=product_id)
            seller = Seller.objects.get(seller_id=request.user)
            if  product.seller_id == seller:
                Product.objects.get(id=product_id).delete()
                return HttpResponseRedirect("/shop/")
            else:
                return HttpResponse("You do not have the required permissions", status=401)
        except:
            return HttpResponse("You do not have the required permissions", status=401)

    # Returns if user is not authenticated
    if not request.user.is_authenticated:
        return HttpResponse("Not authorized", status=401)

    # Return 405 if any other method besides the ones specified above is tried
    return HttpResponse("Method not allowed", status=405)

def output_product(product):
    """
    Returns product dict
    """
    return {
        "Title": product.title,
        "Description": product.description,
        "Price": product.price,
        "Seller": output_seller(product.seller_id),
        "Stock": product.stock,
        "Active": product.active
    }
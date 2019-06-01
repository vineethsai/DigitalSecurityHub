import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from shop.models import Review
from products.models import Product
from products.views import output_product
from accounts.views import output_customer
from accounts.models import Customer
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def shop(request):
    """
    Displays the shop for users to browse.
    GET: Renders items in the shop.
    """
    if request.method == "GET":
        return render(request, "shop/shop.html", {
            "products": Product.objects.all()
        })
    return HttpResponse("Method not allowed on shop/" + product_id, status=405)

@csrf_exempt
def productReview(request, product_id):
    """
    Allows users to view and interact with specific products.
    GET: renders a lists all reviews for product
    POST: adds a review for the product.
    DELETE: removes all reviews for the product if user is an admin.
    """
    # Attemps to get specific product
    try:
        product = Product.objects.get(id=product_id)
    except:
        return HttpResponse("Failed to find product.", status=404)

    if request.method == "GET":
        output_list = []
        rating_sum = 0
        rating_count = 0
        # Outputs JSON response of all methods for given product id
        for review in Review.objects.filter(product_id=product_id):
            output_list.append(output_review(review))
            rating_sum += review.rating
            rating_count += 1

        # Returns json serialized message
        return render(request, "shop/reviewList.html", {
            "reviews": output_list,
            "product": Product.objects.get(id=product_id),
            "avg_rating": 0 if rating_count is 0 else rating_sum / rating_count
        })

    # All other http types require json
    try:
        json_post = json.loads(request.body)
    except:
        return HttpResponse("Failed to process request.", status=500)

    # All other http types require user to be authenitcated
    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if request.method == "POST":
        # Creates a new review
        try:
            new_review = Review.objects.create(
                review_text = json_post["review"],
                rating = json_post["rating"],
                customer_id = Customer.objects.get(customer_id=request.user),
                product_id = product
            )
        except:
            return HttpResponse("Failed to create review", status=500)

        # Returns json serialized message
        return JsonResponse(output_review(new_review), status=201)

    if request.method == "DELETE":
        # Verifies user is admin
        if not request.user.is_superuser:
            return HttpResponse(status=403)

        # Removes all reviews
        for review in Review.objects.filter(product_id=product_id):
            try:
                review.delete()
            except:
                return HttpResponse("Failed to delete all reviews.", status=500)
        return HttpResponse("Reviews Deleted!", status=200)

    return HttpResponse("Method not allowed on shop/" + product_id, status=405)

@csrf_exempt
def specificProductReview(request, review_id):
    """
    Allows user to interact with their review
    GET: renders the specific review
    PATCH: edits review is poster
    DELETE: deletes review if poster
    """
    # Verifies review exists
    try:
        review = Review.objects.get(id=review_id)
    except:
        return HttpResponse("Failed to find review.", status=404)

    if request.method == "GET":
        return render(request, "shop/specificReview.html", {"review": output_review(review)})

    # Verifies user is the owner of the review
    try:
        if review.customer_id.id is not Customer.objects.get(customer_id=request.user).id:
            return HttpResponse(status=403)
    except:
        return HttpResponse("Failed to find Customer.", status=404)

    if request.method == "PATCH":
        # Gets JSON input
        try:
            json_post = json.loads(request.body)
        except:
            return HttpResponse("Failed to load JSON.", status=500)

        # Attempts to edit the message
        try:
            review.review_text = json_post["review"]
            review.save()
        except:
            return HttpResponse("Failed to edit message.", status=500)
        return JsonResponse(output_review(review), status=200)

    if request.method == "DELETE":
        # Deletes review
        try:
            review.delete()
        except:
            return HttpResponse("Failed to delete review.", status=500)
        return HttpResponse("Review Deleted!", status=200)

    return HttpResponse(
        "Method not allowed on shop/" + product_id + "/" + review_id,
        status=405
    )

def output_review(review):
    return {
        "review_text": review.review_text,
        "date_posted": review.date_posted,
        "rating": review.rating,
        "customer_id": output_customer(review.customer_id),
        "product_id": output_product(review.product_id)
    }
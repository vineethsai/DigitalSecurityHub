import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from shop.models import Review
from products.models import Product
from products.views import output_product
from auth.views import output_customer
from auth.models import Customer

# Create your views here.
def productReview(request, product_id):
    """
    Allows users to view and interact with specific products.
    GET: lists all reviews for product
    POST: adds a review for the product.
    DELETE: removes all reviews for the product if user is an admin.
    """
    # Attemps to get specific product
    try:
        product = Product.objects.get(id=product_id)
    except:
        return HttpResponse("Failed to find channel.", status=404)

    if request.method == "GET":
        output_list = []
        # Outputs JSON response of all methods for given product id
        for review in Review.objects.filter(product_id=product_id):
            output_list.append(output_review(review))

        # Returns json serialized message
        return JsonResponse(user_list, safe=False)

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
                customer_id = Customer.objects.get(id=request.user.id),
                product_id = product,
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

def specificProductReview(request, product_id, review_id):
    """
    Allows user to interact with their review
    GET: lists JSON of review for product
    PATCH: edits review is poster
    DELETE: deletes review if poster
    """
    # Verifies review exists
    try:
        review = Review.objects.get(id=review_id)
    except:
        return HttpResponse("Failed to find channel.", status=404)

    if request.method == "GET":
        return JsonResponse(output_review(review), safe=False)

    # Verifies user is the owner of the review
    if review.customer_id.id is not Customer.objects.get(id=request.user.id).id:
        return HttpResponse(status=403)

    if request.method == "PATCH":
        # Gets JSON input
        # All other http types require json
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
        try:
            review.delete()
        except:
            return HttpResponse("Failed to delete review.", status=500)
        return HttpResponse("Review Deleted!", status=200)

    return HttpResponse(
        "Method not allowed on shop/" product_id + "/" + review_id,
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
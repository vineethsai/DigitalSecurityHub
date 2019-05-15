from django.shortcuts import render
from django.views.generic import ListView
from accounts.views import output_seller
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from cart.models import Cart
from accounts.models import Customer
import json
# from django.views import ListView


from .models import Product


def ProductList(request):
    """
    GET: renders JSON of all products
    POST: adds a new product
    DELETE: deletes all products owned by this user
    """
    
    products = Product.objects.all()
    if request.method == 'GET':
        product_list = []

        for item in products:
            product_list.append(output_product(item))
        
        return JsonResponse(product_list, safe=False)
    
    if request.method is 'POST':
        try:
            json_post = json.loads(request.body)
            Product.objects.create(
                title = json_post['title'],
                description = json_post['description'],
                price = json_post['price'],
                seller = json_post['seller'],
                stock = json_post['stock'],
                active = json_post['active']
            )
            return HttpResponse('Product added')

        except:
            return HttpResponse("Failed to process json.", status=500)

    if request.method is 'DELETE':
        try:
            json_post = json.loads(request.body)
            Product.objects.get(id=id).delete()
            return HttpResponse('Product deleted')

        except:
            return HttpResponse("Failed to delete product.", status=500)


def SpecificProduct(request, quantity, product_id):
    """
    GET: renders JSON of specific product
    POST: adds product to cart
    PATCH: edits product information if seller
    DELETE: deletes product if seller
    """
    
    if request.method is 'GET':
        try:
            json_post = json.loads(request.body)
            product = Product.objects.get(id=product_id)
            return JsonResponse(product, safe=False)
        except:
            return HttpResponse('Could not find product')
        
    
    if request.method is 'POST':
        try:
            json_post = json.loads(request.body)
            product = Product.objects.get(
                title = json_post['title'],
                description = json_post['description'],
                price = json_post['price'],
                seller = json_post['seller'],
                stock = json_post['stock'],
                active = json_post['active']
            )
            Cart.object.create(product=product, quantity=quantity, customer_id=request.user)
            return HttpResponse('Product added')
        except:
            return HttpResponse("Could not add product to cart.", status=500)


    if request.method is 'PATCH':
        try:
            json_post = json.loads(request.body)
            product = Product.objects.get(id=product_id)
            product.title = json_post['title']
            product.description = json_post['description']
            product.price = json_post['price']
            product.seller = json_post['seller']
            product.stock = json_post['stock']
            product.active = json_post['active']
            product.save()
            return HttpResponse('Product updated')
        except:
            return HttpResponse('Product could not be updated')


    if request.method is 'DELETE':
        if Customer.objects.get(customer_id=request.user).type:
            Product.objects.get(id=product_id).delete()
            return HttpResponse('Product deleted from store')
        else:
            return HttpResponse('You do not have the required permissions', type=401)
    template_name = "products/list.html"

def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)

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
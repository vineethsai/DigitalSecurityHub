from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import ContactForm
from .models import ContactMessage
from products.models import Product

def home(request):
    return render(request, "index.html", {
        "products": Product.objects.all()[:3].filter()
    })

def about(request):
    return render(request, "home/about.html")

def contact(request):
    if request.method == "GET":
        return render(request, "home/contact.html", {"form": ContactForm})
    elif request.method == "POST":
        form = ContactForm(request.POST)
        try:
            if form.is_valid():
                ContactMessage.objects.create(
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    email=form.cleaned_data["email"],
                    message=form.cleaned_data["message"]
                )
            return HttpResponse("Successfully Created", status=200)
        except:
            return HttpResponse("Oops something went wrong", status=500)
    return HttpResponse("Method not allowed on /accounts/customer.", status=405)

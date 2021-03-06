from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.forms.models import model_to_dict
from .forms import SignupForm, SigninForm, CompanyForm, CustomerForm, DeleteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.debug import sensitive_post_parameters
from .models import Customer, Seller, Company
from django.shortcuts import get_object_or_404
from products.forms import ProductCreationForm

# All of the following views are written by Vineeth
# for keeping type of user in track
# customer vs vendor
user_type = 0

def delete(request):
    """
    GET: Will render the delete account confirmation page.
    """
    if not request.user.is_authenticated:
        return render(request, "error.html", {
            "errorcode": 401,
            "message": "Looks like you don't have permission to view this content!",
        }, status=401)

    if request.method == "GET":
        return render(request, "accounts/delete.html", {
            "form": DeleteForm()
        })
    return HttpResponse("Method not allowed.", status=405)

@sensitive_post_parameters()
def signup(request):
    """
    This form registers user"s to the website
    On "GET" request
    Displays the registration form to the user. Sends HTTP status code 200 (OK).
    On a "POST" request
    Will allow a user to register using a form and the built-in Django database model for a user.
    On any other HTTP request method:
    Return a HTTP response with the message "Method not allowed on auth/register."
    and HTTP status code 405 (Method Not Allowed)
    :param request: request object
    :return: httpResponse
    """
    if request.method == "POST":
        global user_type
        form = SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] != form.cleaned_data["password_conf"]:
                return render(request, "accounts/signup.html", {
                    "form": form,
                    "error": "Passwords did not match."
                }, status=400)
            try:
                # creates user
                User.objects.create_user(username=form.cleaned_data["username"],
                                         email=form.cleaned_data["email"]
                                         , first_name=form.cleaned_data["first_name"],
                                         last_name=form.cleaned_data["last_name"],
                                         password=form.cleaned_data["password"])
                user_type = form.cleaned_data["type"]
                # logs user in
                user = authenticate(request, username=form.cleaned_data["username"],
                                    password=form.cleaned_data["password"])
                if user is not None:
                    login(request, user)
                    # redirects to signup2
                    return HttpResponseRedirect("/accounts/signup2")
                else:
                    return render(request, "accounts/signup.html", {
                        "form": form,
                        "error":"Invalid credentials."
                    }, status=401)
            except:
                return render(request, "accounts/signup.html", {
                    "form": form,
                    "error": "Oops something went wrong"
                }, status=500)
        else:
            return render(request, "accounts/signup.html", {
                "form": form,
                "error": "Invalid registration request."
            }, status=400)
    elif request.method == "GET":
        form = SignupForm()
        return render(request, "accounts/signup.html", {"form": form}, status=200)
    return HttpResponse("Method not allowed on /accounts/register.", status=405)


@sensitive_post_parameters()
def signup2(request):
    """
    On "GET" request
    Displays the registration form to the user. Sends HTTP status code 200 (OK).
    Return a HTTP response with the message "Method not allowed on auth/register."
    and HTTP status code 405 (Method Not Allowed)
    :param request:
    :return:
    """
    # global user_type
    if request.method == "GET":
        vendor_form_1 = CompanyForm()
        customer_form = CustomerForm()
        # renders specific form
        return render(request, "accounts/signup_part2.html",
                      {"vendor_form_1": vendor_form_1,
                       "customer_form": customer_form,
                       "type": user_type}, status=200)
    else:
        return HttpResponse("Method not allowed on /accounts/register.", status=405)


@sensitive_post_parameters()
def vendor(request):
    """
    On a "POST" request
    Will allow a user to register using a form and the built-in Django database model for a user.
    On any other HTTP request method:
    ON "DELETE" reguest, it deletes the vendor from the DB
    Return a HTTP response with the message "Method not allowed on auth/register."
    and HTTP status code 405 (Method Not Allowed)
    :param request:
    :return:
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                vendor_form_1 = CompanyForm(request.POST)
                if vendor_form_1.is_valid():
                    # creates company
                    Company.objects.update_or_create(
                        name=vendor_form_1.cleaned_data["name"],
                        address=vendor_form_1.cleaned_data["address"],
                        city=vendor_form_1.cleaned_data["city"],
                        state=vendor_form_1.cleaned_data["state"],
                        zip=vendor_form_1.cleaned_data["zip"]
                    )
                    # creates seller
                    Seller.objects.update_or_create(name=vendor_form_1.cleaned_data["name"],
                                                    seller_id=request.user,
                                                    company_id=Company.objects.get(
                                                        name=vendor_form_1.cleaned_data["name"]))

                    # create customer
                    Customer.objects.update_or_create(
                        customer_id=request.user,
                        address=vendor_form_1.cleaned_data["address"],
                        city=vendor_form_1.cleaned_data["city"],
                        state=vendor_form_1.cleaned_data["state"],
                        zip=vendor_form_1.cleaned_data["zip"],
                        type=1
                    )
                return HttpResponseRedirect("/")
            except:
                return HttpResponse("Oops something went wrong", status=500)
        else:
            return HttpResponse("Login to continue")

    elif request.method == "DELETE":
        try:
            form = DeleteForm(request.DELETE)
            if request.user.is_authenticated:
                # since ON.delete is set to cascade, deleing user and company should delete the
                # entry from all models
                Company.objects.get(name=form["name"]).delete()
                User.objects.get(id=request.user.id).delete()
        except:
            return HttpResponse("Oops something went wrong", status=500)
    else:
        return HttpResponse("Method not allowed on /accounts/register.", status=405)


@sensitive_post_parameters()
def customer(request):
    """
    On a "POST" request
    Will allow a user to register using a form and the built-in Django database model for a user.
    On any other HTTP request method:
    ON "DELETE" reguest, it deletes the vendor from the DB
    Return a HTTP response with the message "Method not allowed on auth/register."
    and HTTP status code 405 (Method Not Allowed)
    :param request:
    :return:
    """
    if request.method == "POST":
        customer_form = CustomerForm(request.POST)
        if request.user.is_authenticated:
            try:
                # if form is valid, creates user
                if customer_form.is_valid():
                    Customer.objects.update_or_create(
                        customer_id=request.user,
                        address=customer_form.cleaned_data["address"],
                        city=customer_form.cleaned_data["city"],
                        state=customer_form.cleaned_data["state"],
                        zip=customer_form.cleaned_data["zip"],
                        type=user_type
                    )
                return HttpResponseRedirect("/")
            except:
                return HttpResponse("Oops something went wrong", status=500)
        else:
            return HttpResponse("Please log in", status=201)
    elif request.method == "DELETE":
        try:
            # if authenticated, deletes user
            if request.user.is_authenticated:
                User.objects.get(id=request.user.id).delete()
                return HttpResponseRedirect("Successfully Deleted")
            else:
                return HttpResponse("Login to continue")
        except:
            return HttpResponse("Oops something went wrong", status=500)
    else:
        return HttpResponse("Method not allowed on /accounts/customer.", status=405)


@sensitive_post_parameters()
def signin(request):
    """
    This method sign"s users in
    On "GET" request
    Will show the user a form that they can use to signin. Sends HTTP status code 200 (OK).
    On a "POST" request
    On any other HTTP request method:
    Return a HTTP response with the message "Method not allowed on auth/signin." and HTTP status
    code 405 (Method Not Allowed)
    :param request: request object
    :return: httpResponse
    """
    global user_type
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            try:
                form = ProductCreationForm()
                seller = Seller.objects.get(seller_id=request.user)
                return render(request
                                , "accounts/profile.html",
                                {"user": User.objects.get(id=request.user.id),
                                "data": seller.company_id,
                                "user_type": "Company",
                                "form": form,
                                "form_type": "submit"})
            except:
                return render(request
                                , "accounts/profile.html",
                                {"user": User.objects.get(id=request.user.id),
                                "data": Customer.objects.get(customer_id=request.user),
                                "user_type": "Customer",
                                "form_type": "hidden"})
        else:
            form = SigninForm()
            return render(request, "accounts/signin.html", {"form": form}, status=200)
    elif request.method == "POST":
        form = SigninForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    return render(request, "accounts/signin.html", {
                        "form": form,
                        "error": "Invalid credentials."
                    }, status=401)
        except:
            return render(request, "accounts/signin.html", {
                "form": form,
                "error": "Oops something went wrong"
            }, status=500)
        else:
            return render(request, "accounts/signin.html", {
                "form": form,
                "error": "Bad sign in form."
            }, status=400)
    return HttpResponse("Method not allowed on /accounts/signin.", status=405)


@sensitive_post_parameters()
def signout(request):
    """
    This method signs users out
    On "GET" request
    Signout the user if they are logged in.
    On any other HTTP request method:
    Returns a HTTP response with the message "Method not allowed on accounts/signout."
    and HTTP status code 405 (Method Not Allowed)
    :param request: request object
    :return: httpResponse
    """
    if request.method == "GET":
        # checks a logs user out
        if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect("/")
        else:
            return render(request, "error.html", {
                "message": "Not Logged In!",
                "message2": "Try logging in before you log out."
            }, status=404)
    return HttpResponse("Method not allowed on accounts/signout.", status=405)


# Helped fimctions by Quinn
# Create your views here.
def output_user(user):
    """
    Returns output dict for user
    """
    return model_to_dict(user, fields=["id", "username", "first_name", "last_name", "email"])


def output_customer(customer):
    """
    Returns output dict for customer
    """
    return {
        "User": output_user(customer.customer_id),
        "Address": customer.address,
        "City": customer.city,
        "State": customer.state,
        "Zip": customer.zip,
        "Type": customer.type
    }


def output_seller(seller):
    """
    Returns output dict for seller
    """
    return {
        "User": output_user(seller.seller_id),
        "Company": output_company(seller.company_id)
    }


def output_company(company):
    """
    Outputs dict with company information
    """
    return {
        "Name": company.name,
        "Address": company.address
    }

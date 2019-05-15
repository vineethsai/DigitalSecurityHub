from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .forms import SignupForm, SigninForm, CompanyForm, CustomerForm, DeleteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.debug import sensitive_post_parameters
from .models import Customer, Seller, Company

user_type = None


@csrf_exempt
@sensitive_post_parameters()
def signup(request):
    """
    This form registers user's to the website
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
        form = SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] != form.cleaned_data["password_conf"]:
                return HttpResponse("Passwords did not match.", status=400)
            try:
                User.objects.create_user(username=form.cleaned_data["username"],
                                         email=form.cleaned_data["email"]
                                         , first_name=form.cleaned_data["first_name"],
                                         last_name=form.cleaned_data["last_name"],
                                         password=form.cleaned_data["password"])
                user_type = form.cleaned_data['type']
                user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/accounts/signup2")
                else:
                    return HttpResponse("Invalid credentials.", status=401)
            except:
                return HttpResponse("Oops something went wrong", status=500)
        else:
            return HttpResponse("Invalid registration request.", status=400)
    elif request.method == 'GET':
        form = SignupForm()
        return render(request, "accounts/signup.html", {'form': form}, status=200)
    else:
        return HttpResponse("Method not allowed on /accounts/register.", status=405)


@csrf_exempt
@sensitive_post_parameters()
def signup2(request):
    if request.method == 'GET':
        vendor_form_1 = CompanyForm()
        customer_form = CustomerForm()
        return render(request, 'accounts/signup_part2.html',
                      {'vendor_form_1': vendor_form_1,
                       'customer_form': customer_form,
                       'type': user_type}, status=200)
    else:
        return HttpResponse("Method not allowed on /accounts/register.", status=405)


@csrf_exempt
@sensitive_post_parameters()
def vendor(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                vendor_form_1 = CompanyForm(request.POST)
                if vendor_form_1.is_valid():
                    Company.objects.update_or_create(
                        name=vendor_form_1.cleaned_data["name"],
                        address=vendor_form_1.cleaned_data['address'],
                        city=vendor_form_1.cleaned_data['city'],
                        state=vendor_form_1.cleaned_data['state'],
                        zip=vendor_form_1.cleaned_data['zip']
                    )
                    Seller.objects.update_or_create(name=vendor_form_1.cleaned_data["name"],
                                                    seller_id=request.user,
                                                    company_id=Company.objects.get(name=vendor_form_1.cleaned_data["name"]))
                return HttpResponseRedirect('/home')
            except:
                return HttpResponse("Oops something went wrong", status=500)
        else:
            return HttpResponse('Login to continue')

    elif request.method == 'DELETE':
        try:
            form = DeleteForm(request.POST)
            if request.user.is_authenticated:
                Seller.objects.get(seller_id=request.user).delete()
                Company.objects.get(name=form["name"]).delete()
        except:
            return HttpResponse("Oops something went wrong", status=500)
    else:
        return HttpResponse("Method not allowed on /accounts/register.", status=405)


@csrf_exempt
@sensitive_post_parameters()
def customer(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        try:
            if customer_form.is_valid():
                Customer.objects.update_or_create(
                    address=customer_form.cleaned_data['address'],
                    city=customer_form.cleaned_data['city'],
                    state=customer_form.cleaned_data['state'],
                    zip=customer_form.cleaned_data['zip'],
                )
            return HttpResponse('Successfully Created')
        except:
            return HttpResponse("Oops something went wrong", status=500)
    elif request.method == "DELETE":
        try:
            if request.user.is_authenticated:
                Customer.objects.get(customer_id=request.user).delete()
                return HttpResponse('Successfully Deleted')
            else:
                return HttpResponse('Login to continue')
        except:
            return HttpResponse("Oops something went wrong", status=500)
    else:
        return HttpResponse("Method not allowed on /accounts/customer.", status=405)


@csrf_exempt
@sensitive_post_parameters()
def signin(request):
    """
    This method sign's users in
    On "GET" request
    Will show the user a form that they can use to signin. Sends HTTP status code 200 (OK).
    On a "POST" request
    Allows the user to signin using a form and the built-in Django authentication framework by taking t
    he user's username and password and returning a session cookie.
    On any other HTTP request method:
    Return a HTTP response with the message "Method not allowed on auth/signin." and HTTP status
    code 405 (Method Not Allowed)
    :param request: request object
    :return: httpResponse
    """
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request
                          , 'accounts/profile.html',
                          # 'customer': Customer.objects.get(customer_id=request.user),
                          # 'company': Company.objects.get(id=Seller.objects.get(seller_id=request.user).company_id),
                          {'user': User.objects.get(id=request.user.id),
                           'type': user_type})
        form = SigninForm()
        return render(request, "accounts/signin.html", {'form': form}, status=200)
    elif request.method == "POST":
        form = SigninForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return render(request
                                  , 'accounts/profile.html',
                      # 'customer': Customer.objects.get(customer_id=request.user),
                      # 'company': Company.objects.get(id=Seller.objects.get(seller_id=request.user).company_id),
                                  {'user': User.objects.get(id=request.user.id),
                                   'type': user_type})
                else:
                    return HttpResponse("Invalid credentials.", status=401)
        except:
            return HttpResponse("Oops something went wrong", status=500)
        else:
            return HttpResponse("Bad sign in form.", status=400)


@csrf_exempt
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
        if request.user.is_authenticated:
            logout(request)
            return render(request, 'accounts/signout.html')
        else:
            return HttpResponse("Not logged in.", status=200)
    else:
        return HttpResponse("Method not allowed on accounts/signout.", status=405)

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
        "User": output_user(customer.user),
        "BirthDate": customer.birth_date,
        "Address": customer.address,
        "City": customer.city,
        "State": customer.state,
        "Zip": customer.zip
    }

def output_seller(seller):
    """
    Returns output dict for seller
    """
    return {
        "User": output_user(seller.user),
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

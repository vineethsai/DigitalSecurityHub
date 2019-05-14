from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import SignupForm, SigninForm, CompanyForm, SellerForm, CustomerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.debug import sensitive_post_parameters
from .models import Customer, Seller, Company


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
            user = User.objects.create_user(username=form.cleaned_data["username"],
                                            email=form.cleaned_data["email"]
                                            , first_name=form.cleaned_data["first_name"],
                                            last_name=form.cleaned_data["last_name"],
                                            password=form.cleaned_data["password"])
            Customer.objects.get_or_create(customer_id=user, type=form.cleaned_data[
                'type'])
            return HttpResponseRedirect('/accounts/signin')

        else:
            return HttpResponse("Invalid registration request.", status=400)
    elif request.method == 'GET':
        form = SignupForm()
        return render(request, "accounts/signup.html", {'form': form}, status=200)
    else:
        return HttpResponse("Method not allowed on /accounts/register.", status=405)


def signup2(request):
    if request.method == 'GET':
        user = request.user

        vendor_form_1 = CompanyForm()
        vendor_form_2 = SellerForm()
        customer_form = CustomerForm()
        return render(request, 'accounts/signup_part2.html',
                      {'vendor_form_1': vendor_form_1,
                       'vendor_form_2': vendor_form_2,
                       'customer_form': customer_form,
                       'Customer': Customer.objects.get(customer_id=user)}, status=200)
    else:
        return HttpResponse("Method not allowed on /accounts/register.", status=405)


def vendor(request):
    if request.method == 'POST':
        vendor_form_1 = SellerForm(request.POST)
        if vendor_form_1.is_valid():
            company = Company.objects.create_or_update(
                name=vendor_form_1.cleaned_data["name"],
                address=vendor_form_1.changed_data['address'],
                city=vendor_form_1.changed_data['city'],
                state=vendor_form_1.changed_data['state'],
                zip=vendor_form_1.changed_data['zip']
            )
            vendor_form_2 = SellerForm(request.POST)
            if vendor_form_2.is_valid():
                Seller.objects.create_or_update(name=vendor_form_2.cleaned_data["name"],
                                                seller_id=request.user
                                                , birth_date=vendor_form_2.cleaned_data["birth_date"],
                                                company_id=company)
                return HttpResponse('Lit')
    else:
        return HttpResponse("Method not allowed on /accounts/register.", status=405)


def customer(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            Customer.objects.update_or_create(
                customer_id=request.user,
                # birth_date=customer_form.cleaned_data["birth_date"],
                address=customer_form.changed_data['address'],
                city=customer_form.changed_data['city'],
                state=customer_form.changed_data['state'],
                zip=customer_form.changed_data['zip'],
            )
        return HttpResponse('lit')
    else:
        return HttpResponse("Method not allowed on /accounts/register.", status=405)


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
        form = SigninForm()
        return render(request, "accounts/signin.html", {'form': form}, status=200)
    elif request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/accounts/signup2")
            else:
                return HttpResponse("Invalid credentials.", status=401)
        else:
            return HttpResponse("Bad sign in form.", status=400)


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
            return HttpResponse("Sign out successful.", status=200)
        else:
            return HttpResponse("Not logged in.", status=200)
    else:
        return HttpResponse("Method not allowed on accounts/signout.", status=405)

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import SignupForm, LoginForm, CompanyForm, SellerForm, CustomerForm
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
            Customer.objects.get_or_create(customer_id=user.id, type=form.cleaned_data[
                'type'])
            return HttpResponseRedirect('/signup2')

        else:
            return HttpResponse("Invalid registration request.", status=400)
    elif request.method == 'GET':
        form = SignupForm()
        return render(request, "auth/signup.html", {'form': form}, status=200)
    else:
        return HttpResponse("Method not allowed on /auth/register.", status=405)


def signup2(request):
    if request.method == 'GET':
        user = request.user

        vendor_form_1 = CompanyForm()
        vendor_form_2 = SellerForm()
        customer_form = CustomerForm()
        return render(request, 'auth/signup_part2.html',
                      {'vendor_form_1': vendor_form_1,
                       'vendor_form_2': vendor_form_2,
                       'customer_form': customer_form,
                       'Customer': Customer.objects.get(customer_id=user)}, status=200)
    elif request.method == 'POST':
        HttpResponse("is working yo")


@sensitive_post_parameters()
def login(request):
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
        form = LoginForm()
        return render(request, "auth/login.html", {'form': form}, status=200)
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                return HttpResponse("Invalid credentials.", status=401)
        else:
            return HttpResponse("Bad login form.", status=400)


@sensitive_post_parameters()
def signout(request):
    """
    This method signs users out
    On "GET" request
    Signout the user if they are logged in.
    On any other HTTP request method:
    Returns a HTTP response with the message "Method not allowed on auth/signout."
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
        return HttpResponse("Method not allowed on auth/signout.", status=405)

from django.http import HttpResponse
from django.shortcuts import render,redirect

def main(request):
    context = {
        "title":"Hello World!",
        "content":" Welcome to the homepage.",

    }
    # if request.user.is_authenticated():
    #     context["premium_content"] = "YEAHHHHHH"
    return render(request, "main.html", context)


def about_page(request):
    context = {
        "title":"About Page",
        "content":" Welcome to the about page."
    }
    return render(request, "main.html", context)


# def contact_page(request):
#     contact_form = ContactForm(request.POST or None)
#     context = {
#         "title":"Contact",
#         "content":" Welcome to the contact page.",
#         "form": contact_form
#     }
#     if contact_form.is_valid():
#         print(contact_form.cleaned_data)
#     # if request.method == "POST":
#     #     #print(request.POST)
#     #     print(request.POST.get('fullname'))
#     #     print(request.POST.get('email'))
#     #     print(request.POST.get('content'))
#     return render(request, "contact/view.html", context)
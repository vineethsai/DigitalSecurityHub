from django.shortcuts import render

from django.template import RequestContext


def handler404(request, exception):
    return render(request, 'error.html', {
        "errorcode": 404,
        "message": "Oops! This page could not be found!",
        "message2": "Sorry but the page you are looking for does not exist or has been removed."
    }, status=404)


def handler500(request):
    return render(request, 'error.html', {
        "errorcode": 500,
        "message": "Oops! Looks like something right now!",
        "message2": "Maybe try a different page."
    }, status=500)
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
        path('login', views.login, name='Sign in'),
        path('signout', views.signout, name='Sign out'),
        path('signup', views.signup, name='Sign up'),
        path('signup2', views.signup2, name='Sign up part 2'),
        # path('customer', views.customer, name='customer'),
        # path('seller', views.seller, name='seller'),
]

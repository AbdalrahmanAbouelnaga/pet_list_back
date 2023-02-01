from . import views
from django.urls import path



urlpatterns = [
    path('sign-up/',views.sign_up),

]
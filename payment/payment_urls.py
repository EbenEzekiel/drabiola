from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.index, name="index"),
    path('index2', views.index2),
    path("create_checkout_session", views.create_checkout_session, name="create_checkout_session"),
    path("webhook", views.stripe_webhook, name="stripe_webhook"),
    path("registration", views.registration, name="registration"),
    path("registration/status", views.registration_status, name="registration_status"),
]


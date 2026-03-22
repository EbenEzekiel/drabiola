from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Payment


stripe.api_key = settings.STRIPE_SECRETE_KEY

# Create your views here.

def index(request):
    return render(request, 'payment/index.html')

def index2(request):
    return render(request, 'payment/index2.html')

@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        package =  request.POST["selected-package"] #"Silver Package"
        price_list= {
            "Silver Package": "price_1T4gk8JusFC9iYJKWZzeqpXa",
            "Gold Package": "price_1T3xA8JusFC9iYJKoRdVl5Ib",
            "Diamond Package": "price_1T4hCAJusFC9iYJKViuY3i1u"
        }
        print(price_list[package])

        try:
            # Create payment session
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    # "price_data": {
                    #     "currency": "usd",
                    #     "product_data": {
                    #         "name": "AIMSDA Conference Registration",
                    #     },
                    #     "unit_amount": 100000,  # $20.00
                    # },
                    "price":price_list[package] , #"price_1T4hCAJusFC9iYJKViuY3i1u", #,
                    "quantity": 1,
                }],
                mode="payment",
                success_url=settings.SITE_URL + "/registration/status?aimsda-status=success",
                cancel_url=settings.SITE_URL + "/registration/status?aimsda-status=cancelled",
                metadata={
                        # "payer_id": str(payer_id)  # 👈 SEND payer_id here
                        }
            )
            # Insert details into database
            Payment.objects.create(
                name = request.POST.get("name"),
                address = request.POST.get("address"),
                email = request.POST.get("email"),
                organization = request.POST.get("organization"),
                package = request.POST.get("selected-package"),
                requests = request.POST.get("requests"),
                paymentId = session.id,
                paid = False
            )            

            return JsonResponse({"id": session.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def registration(request):
    if request.method == "GET":
        return render(request, "payment/registration.html", {"STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY})

def registration_status(request):
    if request.method == "GET":
        referer = request.META.get("HTTP_REFERER", "")
        sessionid = request.GET.get("session_id", "")
        try:
            id_present = Payment.objects.get(sessionId = sessionid)
        except:
            id_present = None
            return redirect("/")
        if not referer.startswith("https://stripe.com/"):
            return redirect("/")
        # return render(request, "payment/success.html")
        if request.GET.get("aimsda-status") == "success":
            return render(request, "payment/success.html")
        if request.GET.get("aimsda-status") == "cancelled":
            return render(request, "payment/cancel.html")



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # : fulfill the order
        print("Payment successful:", session["id"])
        user = Payment.objects.get(sessionId = session["id"])
        user.paid = True
        user.save()

    return HttpResponse(status=200)
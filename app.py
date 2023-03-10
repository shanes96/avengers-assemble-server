import os
import sys

import stripe
import django
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

# Add the parent directory of your Django project to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avengersassemble.settings')

# Configure the Django settings
django.setup()

# Import the models
from avengersassembleapi.models.cart import Cart

stripe.api_key = 'secret key goes here'

YOUR_DOMAIN = 'http://localhost:8000'

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            # Get the user's cart
            cart_id = request.POST['cart_id']
            cart = Cart.objects.get(id=cart_id)

            # Create the line items for the checkout session
            line_items = []
            for cart_comic in cart.comics.all():
                line_item = {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 1000,
                        'product_data': {
                            'name': cart_comic.title,
                        },
                    },
                    'quantity': 1
                }
                line_items.append(line_item)

            # Create the checkout session
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url='http://localhost:3000/test-payment?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '?canceled=true',
            )

            return redirect(checkout_session.url, code=303)
        except (KeyError, Cart.DoesNotExist):
            return HttpResponseBadRequest('Invalid cart ID')
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    else:
        return HttpResponseBadRequest('Invalid request method')
